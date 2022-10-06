"""
driver file for using google image search with Selenium
1. downloads chromedriver to cache
2. heads to google images and searches for intended images
3. collects and downloads images one-at-a-time
    3a. pulls either at random or specific set of imgs based on config
    3b. scrolls to top of page then to the element in question
    3c. clicks/downloads to appropriate location specified in config
4. exits
"""

import utils.selenium_utils as su
import utils.utils as u
from collections import deque

__author__ = 'jwiebe1017'
__version__ = '1.0.0'
__credits__ = ['stackoverflow', 'me, myself, and I', 'you I guess?']


def main():
    # pull config, setup logging
    data = u.get_config()
    logging = u.logging_setup(
        __name__,
        data['LOGGING_DEBUG_MODE']
    )

    logging.info('Starting...')
    # build url with 'google search' terms embedded
    query = su.build_url(
        data['BASE_URL'],
        data['QUERY_REPL'],
        data['TEMP_SEARCH_STR']
    )

    logging.info(f'{query}')
    # start driver, just use a cached version
    driver = su.webdriver.Chrome(
        service=su.Service(su.ChromeDriverManager().install()),
        desired_capabilities={
            'chromeOptions': {
                "args": data['chrome_settings_args'],
            }
        }
    )
    # head to url, pull pics
    driver.get(query)
    # user is expected to pick either sequential results or totally random results
    if data['RANDOM'] is True:  # pull completely random photos from the webpage
        logging.info('Random Images Selected, Pulling')
        imgs_urls = map(
            lambda rand_elem:
            su.return_img_url(  # pulls img url in 'src' of html
                driver,
                data['IMAGES_BASE'],
                rand_elem,
                data['THUMBNAIL_CLASS_ELEMENT'],
                data['IMG_CLASS_ELEMENT']
            ),
            su.random.sample(  # pulls based on a random int based on # requested in config
                range(
                    0,
                    data['NUMBER_OF_IMAGES'] + 1
                ),
                data['NUMBER_OF_IMAGES']
            )
        )
    else:  # pull X range images from the webpage
        logging.info('Fixed Range of Images Selected, Pulling')
        imgs_urls = map(
            lambda rand_elem:
            su.return_img_url(
                driver,
                data['IMAGES_BASE'],
                rand_elem,
                data['THUMBNAIL_CLASS_ELEMENT'],
                data['IMG_CLASS_ELEMENT']
            ),
            range(
                data['START_RANGE_OF_IMAGES'],
                data['END_NUMBER_OF_IMAGES']
            )
        )

    img_bytes = map(
        su.get_img_content,
        imgs_urls
    )
    # save the images out to designated location
    deque(
        map(
            lambda img_byte:
            su.write_to_file(
                img_byte,
                data['CHROME_DOWNLOAD_DIR'],
                data['FILE_NAME'],
                data['FILE_EXT']
            ),
            img_bytes
        )
    )
    logging.info("Complete")


if __name__ == '__main__':
    main()
