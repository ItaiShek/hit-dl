import sys
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from new_parser import NewParser, NewHelpFormatter


def get_custom_settings(arguments):
    s = {}
    if arguments.verbose:
        s['LOG_LEVEL'] = 'DEBUG'
    if arguments.user_agent:
        s['USER_AGENT'] = arguments.user_agent
    s['COOKIES_ENABLED'] = arguments.cookies_disabled
    s['ROBOTSTXT_OBEY'] = arguments.robots_txt
    return s


def main():
    parser = NewParser(
        description='Download the contents of an entire course from md.hit.ac.il',
        usage='hit-dl -u USERNAME -p PASSWORD URL [URL1 URL2...]\n\n'
              ' e.g.: hit-dl -u student -p pass123 https://md.hit.ac.il/course/view.php?id=12345',
        formatter_class=lambda prog: NewHelpFormatter(prog, max_help_position=27)
    )

    parser.add_argument('-u', '--username', metavar='', required=True, help="your moodle username")
    parser.add_argument('-p', '--password', metavar='', required=True, help="your moodle password")
    parser.add_argument('URL', nargs='+', help="the course/s url/s you want to download")
    parser.add_argument('-v', '--verbose', action='store_true', help='print debugging information')
    parser.add_argument('-r', '--robots-txt', action='store_false', help='disobey ROBOTS.txt')
    parser.add_argument('-a', '--user-agent', metavar='', help='override the default user agent')
    parser.add_argument('-c', '--cookies-disabled', action='store_false', help='disable cookies')

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # set user settings
    custom_settings = get_custom_settings(args)

    # start crawling
    # the next two lines are only for pyinstaller
    settings_file_path = 'settings'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

    settings = get_project_settings()
    settings.update(custom_settings)

    process = CrawlerProcess(settings)

    process.crawl('moodle_spider', username=args.username, password=args.password, urls=args.URL)
    process.start()
    print("\n\nFinished")
    sys.exit(0)


if __name__ == '__main__':
    main()
