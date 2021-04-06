import argparse
import sys
import os
import log
import deploy

VERSION = "v0.8.0"


class MyArgumentParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        if argv:
            msg = ('unrecognized arguments: %s')
            self.error(msg % ' '.join(argv))
        return args

    def print_usage(self, file=None):
        logger = log.Log()
        cmd = ' '.join(sys.argv[1:])
        # path = sundry.get_path()
        # logger.write_to_log('DATA', 'INFO', 'cmd_input', path, {'valid':'1','cmd':cmd})
        # logger.write_to_log('INFO', 'INFO', 'finish','', 'print usage')
        if file is None:
            file = sys.stdout
        self._print_message(self.format_usage(), file)

    def print_help(self, file=None):
        logger = log.Log()
        logger.write_to_log('INFO', 'INFO', 'finish','', 'print help')
        if file is None:
            file = sys.stdout
        self._print_message(self.format_help(), file)



class VtelCLI(object):
    """
    Vtel command line client
    """
    def __init__(self):
        self.parser = MyArgumentParser(prog="vtel")

        self.logger = log.Log()
        # self._replay_commands = ReplayCommands(self.parser)
        self.setup_parser()


    def setup_parser(self):
        # parser = MyArgumentParser(prog="vtel")
        """
        Set parser vtel sub-parser
        """
        subp = self.parser.add_subparsers(metavar='',
                                     dest='subargs_vtel')

        self.parser.add_argument('-v',
                            '--version',
                            dest='version',
                            help='Show current version',
                            action='store_true')

        parser_apply = subp.add_parser(
            'apply',
            help='Apply a configuration file',
        )
        parser_apply.add_argument(
            'file',
            help='Enter the name of the configuration file to be applied(yaml file)')


        # add all subcommands and argument
        # self._replay_commands.setup_commands(subp)
        parser_apply.set_defaults(func=self.fun_apply)
        self.parser.set_defaults(func=self.func_vtel)


    def func_vtel(self,args):
        if args.version:
            print(f'VersaTEL G2 {VERSION}')
        else:
            self.parser.print_help()



    def fun_pv_create(self,args):
        pass


    def fun_apply(self,args):
        if not args.file.endswith('.yaml'):
            print('Please use yaml file')
            return

        iterator_files = os.walk(os.getcwd())
        _, _, files = next(iterator_files)
        if not args.file in files:
            print('The file cannot be found in the current directory')
            return


        conf_data = {'Kind':'11'}

        # 调用执行
        # 1 读取yaml文件数据的cluster
        # 2 读取yaml文件的Kind

        try:
            handler = deploy.ResourceFactory(conf_data['Kind'])
        except Exception:
            pass

        # for data in get_creation():
        #     handler.create(data)






    def parse(self): # 调用入口
        args = self.parser.parse_args()
        path = 'path'
        cmd = ' '.join(sys.argv[1:])
        if args.subargs_vtel:
            if args.subargs_vtel not in ['re', 'replay']:
                self.logger.write_to_log('DATA', 'INPUT', 'cmd_input', path, {'valid': '0', 'cmd': cmd})
        else:
            self.logger.write_to_log('DATA','INPUT','cmd_input', path, {'valid':'0','cmd':cmd})
        args.func(args)


def main():
    try:
        cmd = VtelCLI()
        cmd.parse()
    except KeyboardInterrupt:
        sys.stderr.write("\nClient exiting (received SIGINT)\n")
    except PermissionError:
        sys.stderr.write("\nPermission denied (log file or other)\n")


if __name__ == '__main__':
    main()