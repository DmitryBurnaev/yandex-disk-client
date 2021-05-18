# Simple python package for access to Yandex disk #

This is just simple python SDK for access to YandexDisk 

## How to usage ##

### Get oauth token ### 

https://tech.yandex.ru/oauth/doc/dg/reference/console-client-docpage/

### Create client object and use it ### 

```python
from yandex_disk.rest_client import YandexDiskClient

client = YandexDiskClient('<your_token>')
# "test" - root folder on disk 

# create directory
client.mkdir('/test/test2/')
# upload file
client.upload('/<local file directory>/test.txt', '/test/test.txt')
# copy file
client.copy('/test/test.txt', '/test/test2.txt')
# remove file
client.remove('/test/test2.xlsx')
# move file
client.move('/test/test.txt', '/test/test3.txt')
# get download link
link = client.get_download_link_to_file('/test/test3.txt')
# publish element
client.publish('/test/test3/txt')
```


## License

This product is released under the MIT license. See LICENSE for details.
