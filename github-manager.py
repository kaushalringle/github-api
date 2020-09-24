import argparse
import json
import logging
import requests

class githubPullRequests:
    
    def __init__(
        self,
        arguments
    ):

        self.state = arguments.state
        self.type = arguments.type 
        self.reponame = arguments.reponame
        self.owner = arguments.owner
        self.get_pr_response = None    
        self.github_url = "https://api.github.com/repos/{}/{}/pulls".format(
                self.owner,
                self.reponame
            )

    def get_pull_requests(self):
        """
            https://developer.github.com/v3/pulls/#list-pull-requests

            GET /repos/:owner/:repo/pulls
        """
        
        args = {
            "state" : self.state, 
            "type"  : self.type
        }

        try:
            self.get_pr_response = requests.get(
                self.github_url, 
                params = args
            )

        except Exception as get_pr_exception:
            raise get_pr_exception


    def display_pull_requests(self):
        
        logging.info(
            """
                GitHub Pull Requests Summary

                {} repository has {} {} PR's

            """.format(
                    self.reponame,
                    self.state,
                    len(json.loads(self.get_pr_response.text))
            )
        )

        for pr_details in json.loads(self.get_pr_response.text):

            pr_info = """
                "Id"            : {}
                "Title"         : {}
                "Url"           : {}
                "State"         : {}
                "Last Updated"  : {}
                "Closed at"     : {}
                "User"          : {}
                """.format(
                        pr_details.get('id'),
                        pr_details.get('title'),
                        pr_details.get('html_url'),
                        pr_details.get('state'),
                        pr_details.get('updated_at'),
                        pr_details.get('closed_at'),
                        pr_details.get('user').get('login')
            )

            logging.info(pr_info)


def get_arguments():

    parser = argparse.ArgumentParser(
        description = """

            Github Manager
            Supported features:
            Get list of Pull Requests based on thier state.
        
            """
    )

    parser.add_argument(
        "-r",
        "--reponame",
        required = True,
        help = "Name of the GitHub repository"
    )

    parser.add_argument(
        "-s",
        "--state",
        required = True,
        help = "State of the PR",
        default = "open",
        choices = ["open", "closed", "all"]
    )

    parser.add_argument(
        "-t",
        "--type",
        help = "Type of issue",
        default = "pr",
        choices = ["pr"]
    )

    parser.add_argument(
        "-o",
        "--owner",
        help = "Owner of the repository",
        required = True
    )

    parser.add_argument(
        "-l",
        "--loglevel",
        help = "Loglevel for logs",
        default = "info",
        choices = ["info", "debug"]
    )

    arguments = parser.parse_args()

    return arguments 


def log_config(loglevel):

    logging.basicConfig(
        format = '%(levelname)s:%(message)s',
        level = getattr( logging, loglevel.upper())
    )

    return logging.getLogger()


def main():

    arguments = get_arguments()

    log_config(arguments.loglevel)

    classObj = githubPullRequests(
        arguments
    )

    classObj.get_pull_requests()

    classObj.display_pull_requests()


if __name__ == "__main__":
    main()