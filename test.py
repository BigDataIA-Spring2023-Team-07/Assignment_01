import pytest
from Assignment_01.backend import nexrad_main

def test_link_nexrad_streamlit():
    
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2011/10/10/KBGM/KBGM20111010_000301_V03.gz" == nexrad_main.generateLink("2011", "10", "10", "KBGM", "KBGM20111010_000301_V03.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2010/05/12/KARX/KARX20100512_014240_V03.gz" == nexrad_main.generateLink("2010", "05", "12", "KARX", "KARX20100512_014240_V03.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2000/12/22/KBIS/KBIS20001222_090728.gz" == nexrad_main.generateLink("2000", "12", "22", "KBIS", "KBIS20001222_090728.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2015/08/04/KBYX/KBYX20150804_000940_V06.gz" == nexrad_main.generateLink("2015", "08", "04", "KBYX", "KBYX20150804_000940_V06.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2012/07/17/KAPX/KAPX20120717_013219_V06.gz" == nexrad_main.generateLink("2012", "07", "17", "KAPX", "KAPX20120717_013219_V06.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/1993/11/12/KLWX/KLWX19931112_005128.gz" == nexrad_main.generateLink("1993", "11", "12", "KLWX", "KLWX19931112_005128.gz")