import utils.selenium_utils as su
from collections import deque

__author__ = 'jwiebe1017'
__version__ = '1.0.0'
__credits__ = ['stackoverflow', 'me, myself, and I', 'you I guess?']


def main():
    # pull config
    data = su.get_config()
    # build url with 'google search' terms embedded
    query = su.build_url(data['BASE_URL'], data['QUERY_REPL'], data['TEMP_SEARCH_STR'])
    # start driver, just use a cached version
    driver = su.webdriver.Chrome(service=su.Service(su.ChromeDriverManager().install()))
    # head to url, pull pics
    driver.get(query)
    # user is expected to pick either sequential results or totally random results
    if data['RANDOM'] is True:  # pull completely random photos from the webpage
        imgs_urls = map(lambda rand_elem:
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
        imgs_urls = map(lambda rand_elem:
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

    img_bytes = map(su.get_img_content, imgs_urls)
    deque(
        map(
            lambda img_byte:
            su.write_to_file(
                img_byte,
                data['CHROME_DOWNLOAD_DIR']
            ),
            img_bytes
        )
    )


if __name__ == '__main__':
    main()
