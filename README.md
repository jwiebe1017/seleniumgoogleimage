# Selenium Google Image
This little tool will utilize selenium to perform google image search in chrome  
and store the photos into a designated area  
provided by the user in the config (change that? who knows when you read this...)  

Ultimately - I want to service a ml model by serving it images from the web for  
training as opposed to building a biased model utilizing only me as its training  
reference, or even selectively going after specific images.  

This thing doesn't run headless as sometimes it's necessary to step in and scroll a bit for the driver to execute.  
Not sure if I care enough to fix this as it works pretty smoothly as-is otherwise. 

## Steps
 - download chrome driver to your cache
 - go to google images and search desired images
 - select images via scrolling to the top, scrolling to the image
 - save the image to designated location in config

## requirements
`selenium`  
`yaml`  
`uuid`  
`requests`  
`random`  
`os`  
`collections`  
`time`  
`webdriver_manager`  
