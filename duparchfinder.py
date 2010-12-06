import os
import subprocess
import sys
import re

# the ratio of files that should be unpacked from an archive in order for it to be considered unpacked
REQUIRED_UNPACKING_RATIO = 0.5
UNNECESSARY_ARCHIVE_FOUND_MESSAGE = """Possible unnecessary archive {rar_file} with unpacking ratio {unpacking_ratio:.2%}\n"""
RAR_COMMAND = 'unrar'
LIST_FILES_ONLY_FLAG = 'vb'
FILE_HAS_PART_BEFORE_EXTENSION = re.compile(r'part\d+\.rar$')

def which(program):
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def check_command_line_dependencies():
    for dependency_command in [RAR_COMMAND]:
	if not which(dependency_command):
	    sys.exit(dependency_command + ' missing')

def get_files_in_rar_archive(rar_file_full_path):
    rar_file_listing_command = [RAR_COMMAND, LIST_FILES_ONLY_FLAG, rar_file_full_path]
    rar_contents_process = subprocess.Popen(rar_file_listing_command, stdout=subprocess.PIPE)
    rar_contents_string = rar_contents_process.communicate()[0].rstrip()
    rar_contents_set = set(rar_contents_string.split('\n'))
    return rar_contents_set

def file_has_part_before_extension(file_name):
    return FILE_HAS_PART_BEFORE_EXTENSION.search(file_name)

def file_is_first_rar_part(file_name):
    if file_has_part_before_extension(file_name):
	return file_name.endswith('part01.rar')
    else:
	return file_name.endswith('.rar')
def print_message_if_archive_is_unpacked(rar_file_full_path, dir_file_set):
    if file_is_first_rar_part(rar_file_full_path):
	rar_file_set = set(get_files_in_rar_archive(rar_file_full_path))
	unpacked_file_set = dir_file_set.intersection(rar_file_set)
	unpacking_ratio = float(len(unpacked_file_set)) / len(rar_file_set)
	if unpacking_ratio > REQUIRED_UNPACKING_RATIO:
	    sys.stdout.write(UNNECESSARY_ARCHIVE_FOUND_MESSAGE.format(rar_file=rar_file_full_path,
		unpacking_ratio=unpacking_ratio))

def find_duplicate_archives(search_root):
    dir_entries = os.walk(search_root)

    for (dirpath, dirnames, filenames) in dir_entries:
	dir_file_set = set(os.listdir(dirpath))
	for filename in filenames:
	    rar_file_full_path = os.path.join(dirpath, filename)
	    print_message_if_archive_is_unpacked(rar_file_full_path, dir_file_set)

if __name__ == '__main__':
    search_root = sys.argv[1]
    find_duplicate_archives(search_root)
