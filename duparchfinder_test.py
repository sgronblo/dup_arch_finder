import unittest
import duparchfinder

class DuplicateArchiveFinderTest(unittest.TestCase):
    def test_file_har_part_before_extension(self):
	self.assertTrue(duparchfinder.file_has_part_before_extension('foobar.part01.rar'))
	self.assertFalse(duparchfinder.file_has_part_before_extension('foobar.rar'))

    def test_file_is_first_rar_part(self):
	self.assertTrue(duparchfinder.file_is_first_rar_part('foobar.rar'))
	self.assertTrue(duparchfinder.file_is_first_rar_part('foobar.part01.rar'))
	self.assertFalse(duparchfinder.file_is_first_rar_part('foobar.r02'))
	self.assertFalse(duparchfinder.file_is_first_rar_part('foobar.part02.rar'))

if __name__ == '__main__':
    unittest.main()
