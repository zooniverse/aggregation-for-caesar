from panoptes_aggregation import extractors
from .base_test_class import ExtractorTest

classification = {
    "annotations": [
        {
            "task": "T0",
            "value": [
                {
                    "width": 80.36077880859375,
                    "tool": 0,
                    "0": 0,
                    "details": [],
                    "x": 541.7737426757812,
                    "frame": 0
                }
            ]
        }
    ],
    "metadata": {
        "subject_dimensions": [
            {
                "clientWidth": 444,
                "clientHeight": 333,
                "naturalWidth": 1152,
                "naturalHeight": 864
            }
        ]
    },
    "subject": {
        "metadata": {
            "RA": "121.62522",
            "Dec": "17.42804",
            "URL": "http://skyserver.sdss.org/dr12/en/tools/explore/Summary.aspx?ra=121.62522&dec=17.42804",
            "spiral": "0",
            "elliptical": "1",
            "Distance_Mpc": "481.4064706",
            "SVG_filename": "1237665128518320259.svg",
            "#Published_Redshift": "0.1091188"
        }
    }
}

expected = {
    "galaxy_id": "1237665128518320259",
    "url": "http://skyserver.sdss.org/dr12/en/tools/explore/Summary.aspx?ra=121.62522&dec=17.42804",
    "RA": "121.62522",
    "dec": "17.42804",
    "dist": 481.40647058823527,
    "redshift": 0.1146063992421806,
    "velocity": 34381.91977265418,
    "lambdacen": 438.4527192698966
}

TestI2A = ExtractorTest(
    extractors.i2a_extractor,
    classification,
    expected,
    'Test i2a'
)
