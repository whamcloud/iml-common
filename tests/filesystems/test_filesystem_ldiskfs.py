import mock

from iml_common.test.command_capture_testcase import CommandCaptureTestCase, CommandCaptureCommand
from iml_common.filesystems.filesystem_ldiskfs import FileSystemLdiskfs
from iml_common.blockdevices.blockdevice_linux import BlockDeviceLinux
from tests.data import example_data


class TestFileSystemLdiskfs(CommandCaptureTestCase):
    def setUp(self):
        super(TestFileSystemLdiskfs, self).setUp()

        self.uuid_prop_mock = mock.PropertyMock(return_value='123456789123')
        mock.patch.object(BlockDeviceLinux, 'uuid', self.uuid_prop_mock).start()

        self.type_prop_mock = mock.PropertyMock(return_value='ldiskfs')
        mock.patch.object(BlockDeviceLinux, 'filesystem_type', self.type_prop_mock).start()

        self.patch_init_modules = mock.patch.object(FileSystemLdiskfs, '_initialize_modules')
        self.patch_init_modules.start()

        self.filesystem = FileSystemLdiskfs('ldiskfs', '/dev/sda1')

        self.addCleanup(mock.patch.stopall)

        patcher_time = mock.patch('time.time')
        self.addCleanup(patcher_time.stop)
        self.mock_time = patcher_time.start()
        self.mock_time.return_value = 123.45

        patcher_uname = mock.patch('os.uname')
        self.addCleanup(patcher_uname.stop)
        self.mock_uname = patcher_uname.start()
        self.mock_uname.return_value = ('Linux', 'lotus-31vm4', '4.15.6-300.fc27.x86_64',
                                        '#1 SMP Mon Feb 26 18:43:03 UTC 2018', 'x86_64')

    def test_initialize_modules(self):
        self.patch_init_modules.stop()

        self.add_commands(CommandCaptureCommand(('modprobe', 'osd_ldiskfs'), rc=1),
                          CommandCaptureCommand(('modprobe', 'ldiskfs')))

        self.filesystem._initialize_modules()
        self.assertTrue(self.filesystem._modules_initialized)

        self.assertRanAllCommandsInOrder()

    def _mount_fail_initial(self, fail_code):
        """ Test when initial mount fails, retry succeeds and result returned """
        self._mount_capture_setup_debug()
        self.add_commands(CommandCaptureCommand(('mount', '-t', 'lustre', '/dev/sda1', '/mnt/OST0000'), rc=fail_code,
                                                executions_remaining=1),
                          CommandCaptureCommand(('mount', '-t', 'lustre', '/dev/sda1', '/mnt/OST0000'), rc=0,
                                                executions_remaining=1))
        self._mount_restore_debug()

        self.filesystem.mount('/mnt/OST0000')

        self.assertRanAllCommandsInOrder()

    def _mount_capture_setup_debug(self):
        self.add_commands(CommandCaptureCommand(('lctl', 'get_param', 'debug'), rc=0,
                                                stdout="123", executions_remaining=1),
                          CommandCaptureCommand(('lctl', 'get_param', 'debug_mb'), rc=0,
                                                stdout="456", executions_remaining=1),
                          CommandCaptureCommand(('lctl', 'set_param', 'debug=-1'), rc=0,
                                                executions_remaining=1),
                          CommandCaptureCommand(('lctl', 'set_param', 'debug_mb=400'), rc=0,
                                                executions_remaining=1))

    def _mount_restore_debug(self):
        self.add_commands(CommandCaptureCommand(('lctl', 'set_param', 'debug=123'), rc=0,
                                                executions_remaining=2),
                          CommandCaptureCommand(('lctl', 'set_param', 'debug_mb=456'), rc=0,
                                                executions_remaining=2))

    def test_mount_fail_initial_5(self):
        self._mount_fail_initial(5)

    def test_mount_fail_initial_108(self):
        self._mount_fail_initial(108)

    def test_mount_fail_initial_2(self):
        self._mount_fail_initial(2)

    def _mount_capture_debug_logs(self):
        self.add_commands(CommandCaptureCommand(('lctl dk >/var/log/lustre-debug-final_mount-123.45.log',),
                                                rc=0, executions_remaining=1),
                          CommandCaptureCommand(('ssh', 'lotus-31vm5',
                                                 'lctl dk >/var/log/lustre-debug-final_mount-123.45.log'),
                                                rc=0, executions_remaining=1))

    def test_mount_different_rc_fail_initial(self):
        """ Test when initial mount fails and the rc doesn't cause a retry,
            exception is raised """
        self._mount_capture_setup_debug()
        self.add_commands(CommandCaptureCommand(('mount', '-t', 'lustre',
                                                 '/dev/sda1', '/mnt/OST0000'),
                                                rc=1, executions_remaining=1))
        self._mount_capture_debug_logs()
        self._mount_restore_debug()

        self.assertRaises(RuntimeError, self.filesystem.mount, '/mnt/OST0000')

        self.assertRanAllCommandsInOrder()

    def test_mount_fail_second(self):
        """ Test when initial mount fails and the retry fails, exception is raised """
        self._mount_capture_setup_debug()
        self.add_commands(CommandCaptureCommand(('mount', '-t', 'lustre', '/dev/sda1', '/mnt/OST0000'), rc=5,
                                                executions_remaining=1),
                          CommandCaptureCommand(('mount', '-t', 'lustre', '/dev/sda1', '/mnt/OST0000'), rc=5,
                                                executions_remaining=1))
        self._mount_capture_debug_logs()
        self._mount_restore_debug()

        self.assertRaises(RuntimeError, self.filesystem.mount, '/mnt/OST0000')

        self.assertRanAllCommandsInOrder()

    def test_mkfs_options(self):
        test_target = mock.Mock()
        test_target.inode_size = 512
        test_target.bytes_per_inode = 256
        test_target.inode_count = 1024

        self.assertEqual(['-I 512', '-i 256', '-N 1024'], self.filesystem.mkfs_options(test_target))

    def test_devices_match(self):
        mock_stat = mock.patch('os.stat').start()
        self.filesystem.devices_match('/dev/sda1', '/dev/disk/by-id/link_to_sda1', '123456789123')

        mock_stat.assert_has_calls([mock.call('/dev/sda1'), mock.call('/dev/disk/by-id/link_to_sda1')])

    def test_mkfs(self):
        """ Test returning the correct parameters from mkfs call. Test also partly covers inode methods """
        self.add_commands(CommandCaptureCommand(('mkfs.lustre', '/dev/sda1')),
                          CommandCaptureCommand(('dumpe2fs', '-h', self.filesystem._device_path),
                                                stdout=example_data.dumpe2fs_example_output),
                          CommandCaptureCommand(('dumpe2fs', '-h', self.filesystem._device_path),
                                                stdout=example_data.dumpe2fs_example_output))

        self.assertEqual(self.filesystem.mkfs(None, []),
                         {'uuid': '123456789123',
                          'filesystem_type': 'ldiskfs',
                          'inode_size': 128,
                          'inode_count': 128016})

        self.assertRanAllCommandsInOrder()
