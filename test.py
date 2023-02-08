import pytest
from Assignment_01.backend import nexrad_main

def test_link_nexrad_streamlit():
    
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2011/10/10/KBGM/KBGM20111010_000301_V03.gz" == nexrad_main.generateLink("2011", "10", "10", "KBGM", "KBGM20111010_000301_V03.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2011/06/12/KBGM/KBGM20110612_003045_V03.gz" == nexrad_main.generateLink("2011", "06", "12", "KBGM", "KBGM20110612_003045_V03.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2010/05/12/KARX/KARX20100512_014240_V03.gz" == nexrad_main.generateLink("2010", "05", "12", "KARX", "KARX20100512_014240_V03.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2013/09/02/KABX/KABX20130902_002911_V06.gz" == nexrad_main.generateLink("2013", "09", "02", "KABX", "KABX20130902_002911_V06.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2000/12/22/KBIS/KBIS20001222_090728.gz"     == nexrad_main.generateLink("2000", "12", "22", "KBIS", "KBIS20001222_090728.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2012/02/03/KCCX/KCCX20120203_013605_V03.gz" == nexrad_main.generateLink("2012", "02", "03", "KCCX", "KCCX20120203_013605_V03.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2015/08/04/KBYX/KBYX20150804_000940_V06.gz" == nexrad_main.generateLink("2015", "08", "04", "KBYX", "KBYX20150804_000940_V06.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2012/07/17/KAPX/KAPX20120717_013219_V06.gz" == nexrad_main.generateLink("2012", "07", "17", "KAPX", "KAPX20120717_013219_V06.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2014/09/07/KAPX/KAPX20140907_010223_V06.gz" == nexrad_main.generateLink("2014", "09", "07", "KAPX", "KAPX20140907_010223_V06.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/2008/08/19/KCBW/KCBW20080819_012424_V03.gz" == nexrad_main.generateLink("2008", "08", "19", "KCBW", "KCBW20080819_012424_V03.gz")
    assert "https://noaa-nexrad-level2.s3.amazonaws.com/1993/11/12/KLWX/KLWX19931112_005128.gz"     == nexrad_main.generateLink("1993", "11", "12", "KLWX", "KLWX19931112_005128.gz")
    