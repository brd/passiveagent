### Libraries used

*Base*
[ConfigParser](https://docs.python.org/3/library/configparser.html)

[Sched](https://docs.python.org/3/library/sched.html)

*External*
[Requests](https://docs.python-requests.org/en/master/index.html)

### Other

[Example Config](https://github.com/NagiosEnterprises/ncpa/blob/master/agent/etc/ncpa.cfg)

Test instance: http://192.168.1.37/nrdp/ token: blah

Test service: ...

Example JSON result structure:
```
{
    "checkresults": [
        {
            "host": {
                "hostname": "somehost",
                "state": 0,
                "output": "Everything looks okay! | perfdata=1;"
            }
        },
        {
            "service": {
                "hostname": "somehost",
                "servicename": "someservice",
                "state": 1,
                "output": "WARNING: Danger Will Robinson! | perfdata=1;"
            }
        }
    ]
}
```
