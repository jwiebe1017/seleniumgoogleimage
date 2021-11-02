import utils.selenium_utils as su
from collections import deque


def main():
    data = su.get_config()
    query = su.build_url(data['BASE_URL'], data['QUERY_REPL'], data['TEMP_SEARCH_STR'])

    driver = su.webdriver.Chrome(service=su.Service(su.ChromeDriverManager().install()))

    driver.get(query)
    imgs_on_page = su.collect_images_from_driver(driver, data['IMAGES_BASE'])

    if data['RANDOM'] is True:  # pull completely random photos from the webpage
        imgs_urls = map(lambda rand_elem:
                        su.return_img_url(
                            driver,
                            imgs_on_page,
                            rand_elem,
                            data['THUMBNAIL_CLASS_ELEMENT'],
                            data['IMG_CLASS_ELEMENT']
                        ),
                        su.random.sample(
                            range(
                                0,
                                len(imgs_on_page)
                            ),
                            data['NUMBER_OF_IMAGES']
                        )
                        )
    else:  # pull only the first X images from the webpage
        imgs_urls = map(lambda rand_elem:
                        su.return_img_url(
                            driver,
                            imgs_on_page,
                            rand_elem,
                            data['THUMBNAIL_CLASS_ELEMENT'],
                            data['IMG_CLASS_ELEMENT']
                        ),
                        range(
                            0,
                            data['NUMBER_OF_IMAGES']
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
