#!/usr/bin/python3.4


import yaml
from collections import OrderedDict
import argparse
from subprocess import call


def get_args():
	parser = argparse.ArgumentParser(description='Bumps version number in app.yaml')
	parser.add_argument('version_type', type=str, nargs=1, choices=['major', 'minor', 'maintenance'], help="Change significance")
	parser.add_argument('-c', '--commit', dest='commit', action='store_true', help="Commit version bump to local git repository")
	return parser.parse_args()


def load_app_yaml():
	class OrderedLoader(yaml.SafeLoader):
		pass
	def construct_mapping(loader, node):
		loader.flatten_mapping(node)
		return OrderedDict(loader.construct_pairs(node))
	OrderedLoader.add_constructor(
		yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
		construct_mapping)
	with open('app.yaml') as app_file:
		app_str = app_file.read()
	return yaml.load(app_str, OrderedLoader)


def save_app_yaml(app_conf_dict):
	class OrderedDumperSeqIndented(yaml.SafeDumper):
		def increase_indent(self, flow=False, indentless=False):
			return super(OrderedDumperSeqIndented, self).increase_indent(flow, False)
	def _dict_representer(dumper, data):
		return dumper.represent_mapping(
			yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
			data.items())
	OrderedDumperSeqIndented.add_representer(OrderedDict, _dict_representer)
	with open('app.yaml', 'w') as app_file:
		yaml.dump(app_conf_dict, app_file, OrderedDumperSeqIndented, default_flow_style=False, indent=2)


def get_current_version_numbers(app_conf_dict):
	ver_numbers = str(app_conf_dict.get('version', '0')).split('.')
	ver_numbers.extend([0] * (3 - len(ver_numbers)))
	return map(int, ver_numbers)


def get_printable_version_numbers(version):
	return '.'.join(map(str, version.values()))


def bump_version(version_dict, args_ver_type):
	prev_ver_type = None
	for ver_type in reversed(version_dict):
		if prev_ver_type:
			version_dict[prev_ver_type] = 0
		if args_ver_type == ver_type:
			version_dict[args_ver_type] += 1
			break
		prev_ver_type = ver_type


args = get_args()
app_conf_dict = load_app_yaml()
version = OrderedDict()
version['major'], version['minor'], version['maintenance'] = get_current_version_numbers(app_conf_dict)
print('Previous version: \t%s' % get_printable_version_numbers(version))
bump_version(version, args.version_type[0])
app_conf_dict['version'] = get_printable_version_numbers(version)
save_app_yaml(app_conf_dict)
print('Updated version: \t%s' % get_printable_version_numbers(version))

if args.commit:
	call(['git', 'commit', 'app.yaml', '-m', 'Version bump (%s)' % get_printable_version_numbers(version)])
	print('Version bump committed.')

