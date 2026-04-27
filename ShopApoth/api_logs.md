Total entries: 208
### Endpoint: GET https://api.sa-tech.de/de/app-config/v1?osName=android&osVersion=15&appVersion=4.19.0&environment=prod&deviceType=phone&buildType=release
**Status**: 200
#### Request
*No Body*
#### Response
```json
{
  "general": {
    "appUpdateRequired": false,
    "api": {
      "bully": "https://api.sa-tech.de/",
      "nfc": "https://nfcp.sae.systems"
    },
    "shops": [
      {
        "webUrl": "https://www.shop-apotheke.com",
        "name": "Shop Apotheke",
        "theme": "redcare",
        "id": "DE",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "de-DE"
          },
          {
            "localeISO": "en-DE",
            "mainLanguage": "de-DE"
          },
          {
            "localeISO": "fr-DE",
            "mainLanguage": "de-DE"
          },
          {
            "localeISO": "it-DE",
            "mainLanguage": "de-DE"
          }
        ],
        "api": {
          "lms": "https://api.shop-apotheke.com/api/"
        },
        "selectedShop": false,
        "countryNameKey": "app_shopSel_countryGermany"
      },
      {
        "webUrl": "https://www.shop-apotheke.at",
        "name": "Shop Apotheke",
        "theme": "redcare",
        "id": "AT",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "de-AT"
          },
          {
            "localeISO": "en-AT",
            "mainLanguage": "de-AT"
          },
          {
            "localeISO": "fr-AT",
            "mainLanguage": "de-AT"
          },
          {
            "localeISO": "it-AT",
            "mainLanguage": "de-AT"
          }
        ],
        "api": {
          "lms": "https://api.shop-apotheke.at/api/"
        },
        "selectedShop": false,
        "countryNameKey": "app_shopSel_countryAustria"
      },
      {
        "webUrl": "https://www.redcare-pharmacie.fr",
        "name": "Redcare Pharmacie",
        "theme": "redcare",
        "id": "FR",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "fr-FR"
          },
          {
            "localeISO": "de-FR",
            "mainLanguage": "fr-FR"
          },
          {
            "localeISO": "en-FR",
            "mainLanguage": "fr-FR"
          },
          {
            "localeISO": "it-FR",
            "mainLanguage": "fr-FR"
          }
        ],
        "api": {
          "lms": "https://api.shop-pharmacie.fr/api/"
        },
        "selectedShop": false,
        "countryNameKey": "app_shopSel_countryFrance"
      },
      {
        "webUrl": "https://redcare.it",
        "name": "Redcare",
        "theme": "redcare",
        "id": "IT",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "it-IT"
          },
          {
            "localeISO": "en-IT",
            "mainLanguage": "it-IT"
          },
          {
            "localeISO": "de-IT",
            "mainLanguage": "it-IT"
          },
          {
            "localeISO": "fr-IT",
            "mainLanguage": "it-IT"
          }
        ],
        "api": {
          "lms": "https://api.shop-farmacia.it/api/"
        },
        "selectedShop": false,
        "countryNameKey": "app_shopSel_countryItaly"
      },
      {
        "webUrl": "https://www.farmaline.be",
        "name": "Farmaline",
        "theme": "redcare",
        "id": "BE",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "nl-BE"
          },
          {
            "localeISO": "fr-BE"
          },
          {
            "localeISO": "en-BE",
            "mainLanguage": "nl-BE"
          },
          {
            "localeISO": "de-BE",
            "mainLanguage": "nl-BE"
          }
        ],
        "api": {
          "lms": ""
        },
        "selectedShop": false,
        "countryNameKey": "app_shopSel_countryBelgium"
      },
      {
        "webUrl": "https://www.redcare-apotheke.ch",
        "name": "Redcare Apotheke",
        "theme": "redcare",
        "id": "CH",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "de-CH"
          },
          {
            "localeISO": "fr-CH"
          },
          {
            "localeISO": "en-CH",
            "mainLanguage": "de-CH"
          },
          {
            "localeISO": "it-CH",
            "mainLanguage": "de-CH"
          }
        ],
        "api": {
          "lms": ""
        },
        "selectedShop": false,
        "countryNameKey": "app_shopSel_countrySwitzerland"
      }
    ],
    "whitelistDomains": [
      "www.shop-apotheke.com",
      "www.shop-apotheke.at",
      "www.shop-apotheke.fr",
      "www.shop-apotheke.ch",
      "www.shop-pharmacie.fr",
      "www.shop-farmacia.it",
      "www.farmaline.be",
      "www.redcare.it",
      "www.redcare-apotheke.ch",
      "www.redcare-pharmacie.fr",
      "shop-apotheke.com",
      "shop-apotheke.at",
      "shop-apotheke.fr",
      "shop-apotheke.ch",
      "shop-pharmacie.fr",
      "shop-farmacia.it",
      "farmaline.be",
      "redcare.it",
      "redcare-apotheke.ch",
      "redcare-pharmacie.fr",
      "smapadoo.com",
      "smartpatient.eu",
      "mytherapy.app",
      "mytherapyapp.com",
      "www.medapp.nl",
      "farmaline-be-qs.redteclab.de"
    ],
    "disableHostPinning": true
  },
  "logging": {
    "logz": {
      "endPoint": "listener-eu.logz.io",
      "port": 5052,
      "token": "lvRACwIPYTisIdQhAHCPafxjlSGZdMzy"
    }
  },
  "productDetails": {
    "OTCReviewsEnabled": true,
    "3qVideoPlayerUrl": "https://player.3qsdn.com/js3q.latest.js"
  },
  "medallia": {},
  "now": {
    "platformId": "android"
  },
  "crossSell": {
    "maxItemsToDisplay": 36
  },
  "content": {},
  "cart": {
    "OTCaddtoCartEnabled": true
  },
  "algolia": {
    "facets": [
      {
        "facetId": "pharmaForm",
        "lokaliseKey": "app_search_facet_pharmaForm"
      },
      {
        "facetId": "filterAttributes",
        "lokaliseKey": "app_search_facet_filterAttributes"
      },
      {
        "facetId": "packSize",
        "lokaliseKey": "app_search_facet_packSize"
      },
      {
        "facetId": "manufacturer",
        "lokaliseKey": "app_search_facet_manufacturer"
      },
      {
        "facetId": "price",
        "lokaliseKey": "app_search_facet_price"
      },
      {
        "facetId": "averageRating",
        "lokaliseKey": "app_search_facet_rating"
      },
      {
        "facetId": "activeSubstances",
        "lokaliseKey": "app_search_facet_activeSubstances"
      },
      {
        "facetId": "brandIntern",
        "lokaliseKey": "app_search_facet_brandIntern"
      },
      {
        "facetId": "brandSearch",
        "lokaliseKey": "app_search_facet_brandSearch"
      },
      {
        "facetId": "potency",
        "lokaliseKey": "app_search_facet_potency"
      },
      {
        "facetId": "uv_protection",
        "lokaliseKey": "app_search_facet_uv_protection"
      },
      {
        "facetId": "hair_type_multi",
        "lokaliseKey": "app_search_facet_hair_type_multi"
      },
      {
        "facetId": "skin_type_multi",
        "lokaliseKey": "app_search_facet_skin_type_multi"
      },
      {
        "facetId": "gender",
        "lokaliseKey": "app_search_facet_gender"
      },
      {
        "facetId": "hair_color",
        "lokaliseKey": "app_search_facet_hair_color"
      },
      {
        "facetId": "hair_length",
        "lokaliseKey": "app_search_facet_hair_length"
      },
      {
        "facetId": "haircut",
        "lokaliseKey": "app_search_facet_haircut"
      },
      {
        "facetId": "head_circumference",
        "lokaliseKey": "app_search_facet_head_circumference"
      },
      {
        "facetId": "manufacturing_method",
        "lokaliseKey": "app_search_facet_manufacturing_method"
      },
      {
        "facetId": "life_stage",
        "lokaliseKey": "app_search_facet_life_stage"
      },
      {
        "facetId": "variety",
        "lokaliseKey": "app_search_facet_variety"
      },
      {
        "facetId": "special_needs",
        "lokaliseKey": "app_search_facet_special_needs"
      },
      {
        "facetId": "animal_species",
        "lokaliseKey": "app_search_facet_animal_species"
      },
      {
        "facetId": "voltage",
        "lokaliseKey": "app_search_facet_voltage"
      },
      {
        "facetId": "schuessler_salts",
        "lokaliseKey": "app_search_facet_schuessler_salts"
      },
      {
        "facetId": "language",
        "lokaliseKey": "app_search_facet_language"
      },
      {
        "facetId": "publisher",
        "lokaliseKey": "app_search_facet_publisher"
      },
      {
        "facetId": "author",
        "lokaliseKey": "app_search_facet_author"
      },
      {
        "facetId": "urinary_incontinence",
        "lokaliseKey": "app_search_facet_urinary_incontinence"
      },
      {
        "facetId": "stool_incontinence",
        "lokaliseKey": "app_search_facet_stool_incontinence"
      },
      {
        "facetId": "absorbency",
        "lokaliseKey": "app_search_facet_absorbency"
      },
      {
        "facetId": "lens_types",
        "lokaliseKey": "app_search_facet_lens_types"
      }
    ],
    "apiKey": "0f6879638e11eaa302cec13ed66270a2",
    "applicationId": "58ECUELY50",
    "host": "https://58ecuely50-dsn.algolia.net",
    "proxy": {
      "enabled": true,
      "proxyUrl": "algolia.sae.systems"
    },
    "abTests": {
      "enabled": false
    }
  },
  "prescriptionFreeEnvelopeLink": "https://static.shop-apotheke.com/media/pdf/Freiumschlag-SHOP_APOTHEKE-App.pdf",
  "prescriptionFreeEnvelopeLinkEAV": "https://static.shop-apotheke.com/media/pdf/Freiumschlag-EA-App.pdf",
  "tracking": {
    "econda": {
      "countryId": "android.com",
      "siteId": "app.shop-apotheke.com/android",
      "domain": "app-live.shop-apotheke.com/android"
    }
  },
  "erx": {
    "nfcenabled": false,
    "erxVerificationRegexAndroid": "^Task/[a-zA-Z0-9-._]+/\\$accept\\?ac=[a-zA-Z0-9]{64,128}\\\\*$",
    "erxVerificationRegexiOS": "^Task/[a-zA-Z0-9-._]+/\\$accept\\?ac=[a-zA-Z0-9]{64,128}\\\\*$",
    "autoAppliedVoucher": {
      "code": "rezept2025",
      "amountEur": "10",
      "legalFootNote": "28",
      "voucherCodes": [
        {
          "code": "apperx2p5",
          "value": 2.5
        },
        {
          "code": "apperx5",
          "value": 5
        },
        {
          "code": "apperx7p5",
          "value": 7.5
        },
        {
          "code": "apperx10",
          "value": 10
        },
        {
          "code": "apperx12p5",
          "value": 12.5
        },
        {
          "code": "apperx15",
          "value": 15
        },
        {
          "code": "apperx17p5",
          "value": 17.5
        },
        {
          "code": "apperx20",
          "value": 20
        },
        {
          "code": "apperx22p5",
          "value": 22.5
        },
        {
          "code": "apperx25",
          "value": 25
        },
        {
          "code": "apperx27p5",
          "value": 27.5
        },
        {
          "code": "apperx30",
          "value": 30
        },
        {
          "code": "apperx32p5",
          "value": 32.5
        },
        {
          "code": "apperx35",
          "value": 35
        },
        {
          "code": "apperx37p5",
          "value": 37.5
        },
        {
          "code": "apperx40",
          "value": 40
        },
        {
          "code": "apperx42p5",
          "value": 42.5
        },
        {
          "code": "apperx45",
          "value": 45
        },
        {
          "code": "apperx47p5",
          "value": 47.5
        },
        {
          "code": "apperx50",
          "value": 50
        },
        {
          "code": "apperx52p5",
          "value": 52.5
        },
        {
          "code": "apperx55",
          "value": 55
        },
        {
          "code": "apperx57p5",
          "value": 57.5
        },
        {
          "code": "apperx60",
          "value": 60
        },
        {
          "code": "apperx62p5",
          "value": 62.5
        },
        {
          "code": "apperx65",
          "value": 65
        },
        {
          "code": "apperx67p5",
          "value": 67.5
        },
        {
          "code": "apperx70",
          "value": 70
        },
        {
          "code": "apperx72p5",
          "value": 72.5
        },
        {
          "code": "apperx75",
          "value": 75
        },
        {
          "code": "apperx77p5",
          "value": 77.5
        },
        {
          "code": "apperx80",
          "value": 80
        },
        {
          "code": "apperx82p5",
          "value": 82.5
        },
        {
          "code": "apperx85",
          "value": 85
        },
        {
          "code": "apperx87p5",
          "value": 87.5
        },
        {
          "code": "apperx90",
          "value": 90
        },
        {
          "code": "apperx92p5",
          "value": 92.5
        },
        {
          "code": "apperx95",
          "value": 95
        },
        {
          "code": "apperx97p5",
          "value": 97.5
        },
        {
          "code": "apperx100",
          "value": 100
        },
        {
          "code": "apperx102p5",
          "value": 102.5
        },
        {
          "code": "apperx105",
          "value": 105
        },
        {
          "code": "apperx107p5",
          "value": 107.5
        },
        {
          "code": "apperx110",
          "value": 110
        },
        {
          "code": "apperx112p5",
          "value": 112.5
        },
        {
          "code": "apperx115",
          "value": 115
        },
        {
          "code": "apperx117p5",
          "value": 117.5
        },
        {
          "code": "apperx120",
          "value": 120
        },
        {
          "code": "apperx122p5",
          "value": 122.5
        },
        {
          "code": "apperx125",
          "value": 125
        },
        {
          "code": "apperx127p5",
          "value": 127.5
        },
        {
          "code": "apperx130",
          "value": 130
        },
        {
          "code": "apperx132p5",
          "value": 132.5
        },
        {
          "code": "apperx135",
          "value": 135
        },
        {
          "code": "apperx137p5",
          "value": 137.5
        },
        {
          "code": "apperx140",
          "value": 140
        },
        {
          "code": "apperx142p5",
          "value": 142.5
        },
        {
          "code": "apperx145",
          "value": 145
        },
        {
          "code": "apperx147p5",
          "value": 147.5
        },
        {
          "code": "apperx150",
          "value": 150
        },
        {
          "code": "apperx152p5",
          "value": 152.5
        },
        {
          "code": "apperx155",
          "value": 155
        },
        {
          "code": "apperx157p5",
          "value": 157.5
        },
        {
          "code": "apperx160",
          "value": 160
        },
        {
          "code": "apperx162p5",
          "value": 162.5
        },
        {
          "code": "apperx165",
          "value": 165
        },
        {
          "code": "apperx167p5",
          "value": 167.5
        },
        {
          "code": "apperx170",
          "value": 170
        },
        {
          "code": "apperx172p5",
          "value": 172.5
        },
        {
          "code": "apperx175",
          "value": 175
        },
        {
          "code": "apperx180",
          "value": 180
        },
        {
          "code": "apperx182p5",
          "value": 182.5
        },
        {
          "code": "apperx185",
          "value": 185
        },
        {
          "code": "apperx190",
          "value": 190
        },
        {
          "code": "apperx200",
          "value": 200
        }
      ],
      "voucherTiers": [
        {
          "minValue": 0.01,
          "maxValue": 59.99,
          "tierValue": 2.5
        },
        {
          "minValue": 60,
          "maxValue": 249.99,
          "tierValue": 5
        },
        {
          "minValue": 250,
          "maxValue": 999.99,
          "tierValue": 10
        },
        {
          "minValue": 1000,
          "maxValue": 999999.99,
          "tierValue": 20
        }
      ]
    }
  },
  "parcelLab": {
    "user": "1613555",
    "token": "Zf3BbnVVMp0QNVgbfwhup0uRLFgZKHBdE4woVVJneCviZwJU",
    "apiUrl": "https://api.parcellab.com"
  },
  "adserver": {
    "api": "api.sae.systems"
  },
  "currency": {
    "id": "EUR",
    "symbol": "\u20ac"
  },
  "socialmedia": {},
  "sovendus": {},
  "ownbrands": {},
  "myTherapy": {},
  "supportChat": {
    "availabilityUrl": "https://api.sae-conversational.com/",
    "supportUrl": "https://api.sae-conversational.com/mobileapp?tenant=erx&language=de"
  },
  "showAppTrackingTransparencyApple": true,
  "rc_author_comments": "enabled",
  "secrets_updated_at": "2025-10-17T13:31:56.477Z",
  "_metadata": {
    "filters": {
      "appVersion": "4.19.0",
      "buildType": "release",
      "deviceType": "phone",
      "environment": "prod",
      "osName": "android",
      "osVersion": "15"
    },
    "migrationId": "69c53592ff7a87abb552b456"
  }
}
```

================================================================================

### Endpoint: POST https://android.apis.google.com/c2dm/register3
**Status**: 200
#### Request
```json
X-subtype=129759020696&sender=129759020696&X-app_ver=30196&X-osv=35&X-cliv=fiid-21.1.0&X-gmsv=261533035&X-appid=c_TOVURdSAWBmmZRG24JH9&X-scope=*&X-Goog-Firebase-Installations-Auth=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6IjE6MTI5NzU5MDIwNjk2OmFuZHJvaWQ6MDQwMjVkMGU3MDQ5MTQ0YiIsImV4cCI6MTc3Nzg4Nzk5MywiZmlkIjoiY19UT1ZVUmRTQVdCbW1aUkcyNEpIOSIsInByb2plY3ROdW1iZXIiOjEyOTc1OTAyMDY5Nn0.AB2LPV8wRgIhAMXhuzQ9rdBqcRJs1ekNsB8-quKtpcC0ES24kyiLowShAiEAmyKiD76jbQWAVFqzSxMqwgAGtSwReQxBbYM-eb5Ymig&X-gmp_app_id=1%3A129759020696%3Aandroid%3A04025d0e7049144b&X-firebase-app-name-hash=R1dAH9Ui7M-ynoznwBdw01tLxhI&X-app_ver_name=4.19.0&app=shop.shop_apotheke.com.shopapotheke&device=4191852338812232329&app_ver=30196&gcm_ver=261533035&plat=0&cert=d9019bdeb7633dcd4cda2d7105f9f5c92e3108f1&target_ver=36
```
#### Response
```json
token=c_TOVURdSAWBmmZRG24JH9:APA91bGyWdJ2zDd6wmPBOvQxDBYQeYuk3BQyaviMShhXOi4043UxyKArKckq6UnxtrJv9zRoZwj98aYm-6C9rHNWwI0FnIQmUrabdwjkHG569D-yPFCUGwg
```

================================================================================

### Endpoint: GET https://api.sa-tech.de/de/app-config/v1?countryId=DE&osName=android&osVersion=15&appVersion=4.19.0&language=de-DE&environment=prod&deviceType=phone&buildType=release
**Status**: 200
#### Request
*No Body*
#### Response
```json
{
  "general": {
    "appUpdateRequired": false,
    "api": {
      "bully": "https://api.sa-tech.de/",
      "nfc": "https://nfcp.sae.systems"
    },
    "shops": [
      {
        "webUrl": "https://www.shop-apotheke.com",
        "name": "Shop Apotheke",
        "theme": "redcare",
        "id": "DE",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "de-DE"
          },
          {
            "localeISO": "en-DE",
            "mainLanguage": "de-DE"
          },
          {
            "localeISO": "fr-DE",
            "mainLanguage": "de-DE"
          },
          {
            "localeISO": "it-DE",
            "mainLanguage": "de-DE"
          }
        ],
        "api": {
          "lms": "https://api.shop-apotheke.com/api/"
        },
        "selectedShop": true,
        "countryNameKey": "app_shopSel_countryGermany"
      },
      {
        "webUrl": "https://www.shop-apotheke.at",
        "name": "Shop Apotheke",
        "theme": "redcare",
        "id": "AT",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "de-AT"
          },
          {
            "localeISO": "en-AT",
            "mainLanguage": "de-AT"
          },
          {
            "localeISO": "fr-AT",
            "mainLanguage": "de-AT"
          },
          {
            "localeISO": "it-AT",
            "mainLanguage": "de-AT"
          }
        ],
        "api": {
          "lms": "https://api.shop-apotheke.at/api/"
        },
        "selectedShop": false,
        "countryNameKey": "app_shopSel_countryAustria"
      },
      {
        "webUrl": "https://www.redcare-pharmacie.fr",
        "name": "Redcare Pharmacie",
        "theme": "redcare",
        "id": "FR",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "fr-FR"
          },
          {
            "localeISO": "de-FR",
            "mainLanguage": "fr-FR"
          },
          {
            "localeISO": "en-FR",
            "mainLanguage": "fr-FR"
          },
          {
            "localeISO": "it-FR",
            "mainLanguage": "fr-FR"
          }
        ],
        "api": {
          "lms": "https://api.shop-pharmacie.fr/api/"
        },
        "selectedShop": false,
        "countryNameKey": "app_shopSel_countryFrance"
      },
      {
        "webUrl": "https://redcare.it",
        "name": "Redcare",
        "theme": "redcare",
        "id": "IT",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "it-IT"
          },
          {
            "localeISO": "en-IT",
            "mainLanguage": "it-IT"
          },
          {
            "localeISO": "de-IT",
            "mainLanguage": "it-IT"
          },
          {
            "localeISO": "fr-IT",
            "mainLanguage": "it-IT"
          }
        ],
        "api": {
          "lms": "https://api.shop-farmacia.it/api/"
        },
        "selectedShop": false,
        "countryNameKey": "app_shopSel_countryItaly"
      },
      {
        "webUrl": "https://www.farmaline.be",
        "name": "Farmaline",
        "theme": "redcare",
        "id": "BE",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "nl-BE"
          },
          {
            "localeISO": "fr-BE"
          },
          {
            "localeISO": "en-BE",
            "mainLanguage": "nl-BE"
          },
          {
            "localeISO": "de-BE",
            "mainLanguage": "nl-BE"
          }
        ],
        "api": {
          "lms": ""
        },
        "selectedShop": false,
        "countryNameKey": "app_shopSel_countryBelgium"
      },
      {
        "webUrl": "https://www.redcare-apotheke.ch",
        "name": "Redcare Apotheke",
        "theme": "redcare",
        "id": "CH",
        "webViewShop": false,
        "languages": [
          {
            "localeISO": "de-CH"
          },
          {
            "localeISO": "fr-CH"
          },
          {
            "localeISO": "en-CH",
            "mainLanguage": "de-CH"
          },
          {
            "localeISO": "it-CH",
            "mainLanguage": "de-CH"
          }
        ],
        "api": {
          "lms": ""
        },
        "selectedShop": false,
        "countryNameKey": "app_shopSel_countrySwitzerland"
      }
    ],
    "whitelistDomains": [
      "www.shop-apotheke.com",
      "www.shop-apotheke.at",
      "www.shop-apotheke.fr",
      "www.shop-apotheke.ch",
      "www.shop-pharmacie.fr",
      "www.shop-farmacia.it",
      "www.farmaline.be",
      "www.redcare.it",
      "www.redcare-apotheke.ch",
      "www.redcare-pharmacie.fr",
      "shop-apotheke.com",
      "shop-apotheke.at",
      "shop-apotheke.fr",
      "shop-apotheke.ch",
      "shop-pharmacie.fr",
      "shop-farmacia.it",
      "farmaline.be",
      "redcare.it",
      "redcare-apotheke.ch",
      "redcare-pharmacie.fr",
      "smapadoo.com",
      "smartpatient.eu",
      "mytherapy.app",
      "mytherapyapp.com",
      "www.medapp.nl",
      "farmaline-be-qs.redteclab.de"
    ],
    "disableHostPinning": true
  },
  "logging": {
    "logz": {
      "endPoint": "listener-eu.logz.io",
      "port": 5052,
      "token": "lvRACwIPYTisIdQhAHCPafxjlSGZdMzy"
    }
  },
  "productDetails": {
    "retailPriceLegalNo": "1",
    "pricingDiscountLegalNumber": "2",
    "cheapestPricingDiscountLegalNumber": "16",
    "OTCReviewsEnabled": true,
    "3qVideoPlayerUrl": "https://player.3qsdn.com/js3q.latest.js"
  },
  "onlineDoctorService": {
    "questionnaireUrl": "https://www.shop-apotheke.com/webview/online-arzt-service/rezept-anfragen/",
    "consultationUrl": "https://www.shop-apotheke.com/webview/online-arzt-service/videosprechstunde-vereinbaren/",
    "nearbyDoctorUrl": "https://arztsuche.116117.de/pages/arztsuche.xhtml"
  },
  "medallia": {
    "formId": "6319",
    "formIdDrrSurveyAndroid": "26621"
  },
  "now": {
    "platformId": "android",
    "shopId": "shop-apotheke.com",
    "urlInfoLayer": "https://now.shop-apotheke.com/info/{shop}/{platform}?",
    "urlApiWrapper": "https://www.shop-apotheke.com/apiwrapper/",
    "urlDeliveryInfo": "https://now.shop-apotheke.com/now/api/info/shop-apotheke.com",
    "enabled": true
  },
  "crossSell": {
    "aid": "000016f3-496c2984-7951-4ed2-b556-1bdfdd0856c4-8",
    "widLastSeen": 642,
    "widStartpageTopseller": 336,
    "widStartpageTopOffers": 640,
    "widStartpageNewProducts": 337,
    "widStartpageNewInStock": 641,
    "widCategories": 607,
    "widCategoriesNovelties": 601,
    "widProductCrosssell": 338,
    "widCartDrawer": 334,
    "widCartEmpty": 347,
    "widCartFilled": 320,
    "widErxCartIntermediateFirst": 626,
    "widErxCartIntermediateSecond": 627,
    "widErxCartIntermediateThird": 628,
    "widProductAlternative": 298,
    "widCategoriesVariantA": 607,
    "widCategoriesVariantB": 601,
    "maxItemsToDisplay": 36
  },
  "content": {
    "faqUrl": "https://www.shop-apotheke.com/webview/faq",
    "termsUrl": "https://www.shop-apotheke.com/webview/rechtliches/versandapotheke_agb/",
    "privacyUrl": "https://www.shop-apotheke.com/webview/rechtliches/datenschutz/",
    "imprintUrl": "https://www.shop-apotheke.com/webview/rechtliches/apotheke_impressum/",
    "generalConditionsUrl": "https://www.shop-apotheke.com/webview/rechtliches/apotheke_haftung/",
    "creditCheckAnchor": "bonitaet",
    "disclaimerAnchor": "widerruf",
    "legalNotesUrl": "https://www.shop-apotheke.com/webclient/assets/iframe/com/de/legal.html",
    "redpointsTermsUrl": "https://www.shop-apotheke.com/webview/redpoints/teilnahmebedingungen/"
  },
  "cart": {
    "totalSavingsLegalNoticeIndex": "5",
    "collectiveOrderEnabled": true,
    "OTCaddtoCartEnabled": true
  },
  "algolia": {
    "facets": [
      {
        "facetId": "pharmaForm",
        "lokaliseKey": "app_search_facet_pharmaForm"
      },
      {
        "facetId": "filterAttributes",
        "lokaliseKey": "app_search_facet_filterAttributes"
      },
      {
        "facetId": "packSize",
        "lokaliseKey": "app_search_facet_packSize"
      },
      {
        "facetId": "manufacturer",
        "lokaliseKey": "app_search_facet_manufacturer"
      },
      {
        "facetId": "price",
        "lokaliseKey": "app_search_facet_price"
      },
      {
        "facetId": "averageRating",
        "lokaliseKey": "app_search_facet_rating"
      },
      {
        "facetId": "activeSubstances",
        "lokaliseKey": "app_search_facet_activeSubstances"
      },
      {
        "facetId": "brandIntern",
        "lokaliseKey": "app_search_facet_brandIntern"
      },
      {
        "facetId": "brandSearch",
        "lokaliseKey": "app_search_facet_brandSearch"
      },
      {
        "facetId": "potency",
        "lokaliseKey": "app_search_facet_potency"
      },
      {
        "facetId": "uv_protection",
        "lokaliseKey": "app_search_facet_uv_protection"
      },
      {
        "facetId": "hair_type_multi",
        "lokaliseKey": "app_search_facet_hair_type_multi"
      },
      {
        "facetId": "skin_type_multi",
        "lokaliseKey": "app_search_facet_skin_type_multi"
      },
      {
        "facetId": "gender",
        "lokaliseKey": "app_search_facet_gender"
      },
      {
        "facetId": "hair_color",
        "lokaliseKey": "app_search_facet_hair_color"
      },
      {
        "facetId": "hair_length",
        "lokaliseKey": "app_search_facet_hair_length"
      },
      {
        "facetId": "haircut",
        "lokaliseKey": "app_search_facet_haircut"
      },
      {
        "facetId": "head_circumference",
        "lokaliseKey": "app_search_facet_head_circumference"
      },
      {
        "facetId": "manufacturing_method",
        "lokaliseKey": "app_search_facet_manufacturing_method"
      },
      {
        "facetId": "life_stage",
        "lokaliseKey": "app_search_facet_life_stage"
      },
      {
        "facetId": "variety",
        "lokaliseKey": "app_search_facet_variety"
      },
      {
        "facetId": "special_needs",
        "lokaliseKey": "app_search_facet_special_needs"
      },
      {
        "facetId": "animal_species",
        "lokaliseKey": "app_search_facet_animal_species"
      },
      {
        "facetId": "voltage",
        "lokaliseKey": "app_search_facet_voltage"
      },
      {
        "facetId": "schuessler_salts",
        "lokaliseKey": "app_search_facet_schuessler_salts"
      },
      {
        "facetId": "language",
        "lokaliseKey": "app_search_facet_language"
      },
      {
        "facetId": "publisher",
        "lokaliseKey": "app_search_facet_publisher"
      },
      {
        "facetId": "author",
        "lokaliseKey": "app_search_facet_author"
      },
      {
        "facetId": "urinary_incontinence",
        "lokaliseKey": "app_search_facet_urinary_incontinence"
      },
      {
        "facetId": "stool_incontinence",
        "lokaliseKey": "app_search_facet_stool_incontinence"
      },
      {
        "facetId": "absorbency",
        "lokaliseKey": "app_search_facet_absorbency"
      },
      {
        "facetId": "lens_types",
        "lokaliseKey": "app_search_facet_lens_types"
      }
    ],
    "apiKey": "0f6879638e11eaa302cec13ed66270a2",
    "applicationId": "58ECUELY50",
    "suggestIndex": {
      "indexId": "products_prod_DE_de",
      "lokaliseKey": "suggestion"
    },
    "suggestIndexMarketPlace": {
      "indexId": "products_mktplc_prod_DE_de",
      "lokaliseKey": "suggestion"
    },
    "keyWordsSuggestIndex": {
      "indexId": "suggest_products_prod_DE_de",
      "lokaliseKey": "suggestion"
    },
    "host": "https://58ecuely50-dsn.algolia.net",
    "indices": [
      {
        "indexId": "products_prod_DE_de",
        "lokaliseKey": "app_search_index_relevance"
      },
      {
        "indexId": "products_prod_DE_de_price_asc",
        "lokaliseKey": "app_search_index_priceAsc"
      },
      {
        "indexId": "products_prod_DE_de_price_desc",
        "lokaliseKey": "app_search_index_priceDesc"
      },
      {
        "indexId": "products_prod_DE_de_productName_asc",
        "lokaliseKey": "app_search_index_productNameAsc"
      },
      {
        "indexId": "products_prod_DE_de_productName_desc",
        "lokaliseKey": "app_search_index_productNameDesc"
      },
      {
        "indexId": "products_prod_DE_de_topsellerCount_desc",
        "lokaliseKey": "app_search_index_topsellerDesc"
      }
    ],
    "indicesMarketPlace": [
      {
        "indexId": "products_mktplc_prod_DE_de",
        "lokaliseKey": "app_search_index_relevance"
      },
      {
        "indexId": "products_mktplc_prod_DE_de_price_asc",
        "lokaliseKey": "app_search_index_priceAsc"
      },
      {
        "indexId": "products_mktplc_prod_DE_de_price_desc",
        "lokaliseKey": "app_search_index_priceDesc"
      },
      {
        "indexId": "products_mktplc_prod_DE_de_topsellerCount_desc",
        "lokaliseKey": "app_search_index_topsellerDesc"
      },
      {
        "indexId": "products_mktplc_prod_DE_de_Novelties",
        "lokaliseKey": "app_search_index_novelties"
      }
    ],
    "proxy": {
      "enabled": true,
      "proxyUrl": "algolia.sae.systems"
    },
    "abTests": {
      "enabled": false
    }
  },
  "prescriptionFreeEnvelopeLink": "https://static.shop-apotheke.com/media/pdf/Freiumschlag-SHOP_APOTHEKE-App.pdf",
  "prescriptionFreeEnvelopeLinkEAV": "https://static.shop-apotheke.com/media/pdf/Freiumschlag-EA-App.pdf",
  "tracking": {
    "econda": {
      "countryId": "android.com",
      "siteId": "app.shop-apotheke.com/android",
      "domain": "app-live.shop-apotheke.com/android"
    }
  },
  "erx": {
    "enabled": true,
    "nfcenabled": true,
    "erxVerificationRegexAndroid": "^Task/[a-zA-Z0-9-._]+/\\$accept\\?ac=[a-zA-Z0-9]{64,128}\\\\*$",
    "erxVerificationRegexiOS": "^Task/[a-zA-Z0-9-._]+/\\$accept\\?ac=[a-zA-Z0-9]{64,128}\\\\*$",
    "autoAppliedVoucher": {
      "code": "rezept2025",
      "amountEur": "10",
      "legalFootNote": "28",
      "voucherCodes": [
        {
          "code": "apperx2p5",
          "value": 2.5
        },
        {
          "code": "apperx5",
          "value": 5
        },
        {
          "code": "apperx7p5",
          "value": 7.5
        },
        {
          "code": "apperx10",
          "value": 10
        },
        {
          "code": "apperx12p5",
          "value": 12.5
        },
        {
          "code": "apperx15",
          "value": 15
        },
        {
          "code": "apperx17p5",
          "value": 17.5
        },
        {
          "code": "apperx20",
          "value": 20
        },
        {
          "code": "apperx22p5",
          "value": 22.5
        },
        {
          "code": "apperx25",
          "value": 25
        },
        {
          "code": "apperx27p5",
          "value": 27.5
        },
        {
          "code": "apperx30",
          "value": 30
        },
        {
          "code": "apperx32p5",
          "value": 32.5
        },
        {
          "code": "apperx35",
          "value": 35
        },
        {
          "code": "apperx37p5",
          "value": 37.5
        },
        {
          "code": "apperx40",
          "value": 40
        },
        {
          "code": "apperx42p5",
          "value": 42.5
        },
        {
          "code": "apperx45",
          "value": 45
        },
        {
          "code": "apperx47p5",
          "value": 47.5
        },
        {
          "code": "apperx50",
          "value": 50
        },
        {
          "code": "apperx52p5",
          "value": 52.5
        },
        {
          "code": "apperx55",
          "value": 55
        },
        {
          "code": "apperx57p5",
          "value": 57.5
        },
        {
          "code": "apperx60",
          "value": 60
        },
        {
          "code": "apperx62p5",
          "value": 62.5
        },
        {
          "code": "apperx65",
          "value": 65
        },
        {
          "code": "apperx67p5",
          "value": 67.5
        },
        {
          "code": "apperx70",
          "value": 70
        },
        {
          "code": "apperx72p5",
          "value": 72.5
        },
        {
          "code": "apperx75",
          "value": 75
        },
        {
          "code": "apperx77p5",
          "value": 77.5
        },
        {
          "code": "apperx80",
          "value": 80
        },
        {
          "code": "apperx82p5",
          "value": 82.5
        },
        {
          "code": "apperx85",
          "value": 85
        },
        {
          "code": "apperx87p5",
          "value": 87.5
        },
        {
          "code": "apperx90",
          "value": 90
        },
        {
          "code": "apperx92p5",
          "value": 92.5
        },
        {
          "code": "apperx95",
          "value": 95
        },
        {
          "code": "apperx97p5",
          "value": 97.5
        },
        {
          "code": "apperx100",
          "value": 100
        },
        {
          "code": "apperx102p5",
          "value": 102.5
        },
        {
          "code": "apperx105",
          "value": 105
        },
        {
          "code": "apperx107p5",
          "value": 107.5
        },
        {
          "code": "apperx110",
          "value": 110
        },
        {
          "code": "apperx112p5",
          "value": 112.5
        },
        {
          "code": "apperx115",
          "value": 115
        },
        {
          "code": "apperx117p5",
          "value": 117.5
        },
        {
          "code": "apperx120",
          "value": 120
        },
        {
          "code": "apperx122p5",
          "value": 122.5
        },
        {
          "code": "apperx125",
          "value": 125
        },
        {
          "code": "apperx127p5",
          "value": 127.5
        },
        {
          "code": "apperx130",
          "value": 130
        },
        {
          "code": "apperx132p5",
          "value": 132.5
        },
        {
          "code": "apperx135",
          "value": 135
        },
        {
          "code": "apperx137p5",
          "value": 137.5
        },
        {
          "code": "apperx140",
          "value": 140
        },
        {
          "code": "apperx142p5",
          "value": 142.5
        },
        {
          "code": "apperx145",
          "value": 145
        },
        {
          "code": "apperx147p5",
          "value": 147.5
        },
        {
          "code": "apperx150",
          "value": 150
        },
        {
          "code": "apperx152p5",
          "value": 152.5
        },
        {
          "code": "apperx155",
          "value": 155
        },
        {
          "code": "apperx157p5",
          "value": 157.5
        },
        {
          "code": "apperx160",
          "value": 160
        },
        {
          "code": "apperx162p5",
          "value": 162.5
        },
        {
          "code": "apperx165",
          "value": 165
        },
        {
          "code": "apperx167p5",
          "value": 167.5
        },
        {
          "code": "apperx170",
          "value": 170
        },
        {
          "code": "apperx172p5",
          "value": 172.5
        },
        {
          "code": "apperx175",
          "value": 175
        },
        {
          "code": "apperx180",
          "value": 180
        },
        {
          "code": "apperx182p5",
          "value": 182.5
        },
        {
          "code": "apperx185",
          "value": 185
        },
        {
          "code": "apperx190",
          "value": 190
        },
        {
          "code": "apperx200",
          "value": 200
        }
      ],
      "voucherTiers": [
        {
          "minValue": 0.01,
          "maxValue": 59.99,
          "tierValue": 2.5
        },
        {
          "minValue": 60,
          "maxValue": 249.99,
          "tierValue": 5
        },
        {
          "minValue": 250,
          "maxValue": 999.99,
          "tierValue": 10
        },
        {
          "minValue": 1000,
          "maxValue": 999999.99,
          "tierValue": 20
        }
      ]
    }
  },
  "parcelLab": {
    "user": "1613555",
    "token": "Zf3BbnVVMp0QNVgbfwhup0uRLFgZKHBdE4woVVJneCviZwJU",
    "apiUrl": "https://api.parcellab.com"
  },
  "adserver": {
    "api": "api.sae.systems"
  },
  "prescriptionVideoERX": "https://sdn-global-prog-cache.3qsdn.com/2538/files/22/11/18/6798823/1-kGFB3NDrwQLnRfjvTYXz.mp4",
  "prescriptionVideoGeneral": "https://sdn-global-prog-cache.3qsdn.com/2538/files/20/06/1560239/1-gGjyZHWvr4XPYRdfkBh2.mp4",
  "currency": {
    "id": "EUR",
    "symbol": "\u20ac"
  },
  "socialmedia": {
    "urls": {
      "facebook": "https://www.facebook.com/shopapothekecom/",
      "instagram": "https://instagram.com/shopapothekecom",
      "youtube": "https://www.youtube.com/channel/UCbJ7e_ABSL4eh6KvUlcSUrg"
    }
  },
  "customerServiceInfo": {
    "timezone": "Europe/Berlin",
    "serviceHours": [
      {
        "days": [
          0,
          1,
          2,
          3,
          4,
          5
        ],
        "times": {
          "startHour": 8,
          "startMinutes": 0,
          "endHour": 20,
          "endMinutes": 0
        }
      }
    ],
    "hotlinePhoneNumber": "030 3080 6600"
  },
  "pharmaServiceInfo": {
    "timezone": "Europe/Berlin",
    "serviceHours": [
      {
        "days": [
          0,
          1,
          2,
          3,
          4
        ],
        "times": {
          "startHour": 8,
          "startMinutes": 0,
          "endHour": 18,
          "endMinutes": 0
        }
      },
      {
        "days": [
          5
        ],
        "times": {
          "startHour": 8,
          "startMinutes": 0,
          "endHour": 16,
          "endMinutes": 30
        }
      }
    ],
    "hotlinePhoneNumber": "0800 200 800 335"
  },
  "sovendus": {
    "TRAFFIC_MEDIUM_NUMBER": "1",
    "TRAFFIC_SOURCE_NUMBER": "6293",
    "enabled": true
  },
  "ownbrands": {
    "brands": [
      {
        "name": "Redcare",
        "brandCode": "csd03758"
      },
      {
        "name": "Skintist",
        "brandCode": "csd05212"
      },
      {
        "name": "nu3",
        "brandCode": "csd03158"
      },
      {
        "name": "Beavita",
        "brandCode": "csd03163"
      }
    ]
  },
  "myTherapy": {
    "mytherapyFallbackLink": "https://activate.mytherapyapp.com/747790",
    "myTherapyOrderConf": "https://activate.mytherapy.app/mmeT?deep_link_value=mytherapy%3A%2F%2Ftoday&af_dp=mytherapy%3A%2F%2Ftoday&af_xp=custom&pid=SAE-APP&c=MyT_REF_SAE-APP_DE_00_GEN_All_OC-AS-2502&af_android_store_csl=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Deu.smartpatient.mytherapy%26listing%3Dmytherapy-for-shopapotheke&af_ios_store_cpp=8d6e14bd-5a7c-4954-9da6-8b39a4b87a81",
    "myTherapyOrderDetails": "https://activate.mytherapy.app/mmeT?deep_link_value=mytherapy%3A%2F%2Ftoday&af_dp=mytherapy%3A%2F%2Ftoday&af_xp=custom&pid=SAE-APP&c=MyT_REF_SAE-APP_DE_00_GEN_all_OrdDet-AS-2502&af_android_store_csl=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Deu.smartpatient.mytherapy%26listing%3Dmytherapy-for-shopapotheke&af_ios_store_cpp=8d6e14bd-5a7c-4954-9da6-8b39a4b87a81",
    "myTherapyRedPoints": "https://activate.mytherapyapp.com/x1per0"
  },
  "supportChat": {
    "availabilityUrl": "https://api.sae-conversational.com/",
    "supportUrl": "https://api.sae-conversational.com/mobileapp?tenant=erx&language=de"
  },
  "callBackService": {
    "entryUrl": "https://my.meetergo.com/form/bc1032b3-db0b-4efb-8af4-35aa1af07c1a",
    "exitUrl": "https://www.shop-apotheke.com/rueckruf-service/bestaetigung"
  },
  "showAppTrackingTransparencyApple": true,
  "rc_author_comments": "enabled",
  "secrets_updated_at": "2025-10-17T13:31:56.477Z",
  "_metadata": {
    "filters": {
      "appVersion": "4.19.0",
      "buildType": "release",
      "countryId": "DE",
      "deviceType": "phone",
      "environment": "prod",
      "language": "de-DE",
      "osName": "android",
      "osVersion": "15"
    },
    "tenant": "com",
    "migrationId": "69c53592ff7a87abb552b456"
  }
}
```

================================================================================

### Endpoint: POST https://jsi4pf.register.appsflyersdk.com/api/v6.18/androidevent?app_id=shop.shop_apotheke.com.shopapotheke&buildnumber=6.18.0
**Status**: 200
#### Request
```json
{"devkey":"dywcBD4LYRvrB5i4NmhhRM","operator":"","advertiserId":"f51ee336-e489-4882-8c21-95ff06ed4a9a","network":"WIFI","app_name":"Shop Apotheke","uid":"1777283197569-3448301883485198145","carrier":"","app_version_code":"30196","installDate":"2026-04-27_094624+0000","af_gcm_token":"c_TOVURdSAWBmmZRG24JH9:APA91bGyWdJ2zDd6wmPBOvQxDBYQeYuk3BQyaviMShhXOi4043UxyKArKckq6UnxtrJv9zRoZwj98aYm-6C9rHNWwI0FnIQmUrabdwjkHG569D-yPFCUGwg","launch_counter":"0","model":"Pixel 7","sdk":"35","app_version_name":"4.19.0","brand":"google"}
```
#### Response
```json
OK
```

================================================================================

### Endpoint: GET https://api.sa-tech.de/auth/v1/com/login/guest
**Status**: 201
#### Request
*No Body*
#### Response
```json
{
  "tokenType": "bearer",
  "token": "eyJraWQiOiJmMjI3MGU4OS1iOGJjLTQ1ODAtOTA2MC01OTBmMTNiYjkyMjEiLCJhbGciOiJSUzM4NCJ9.eyJleHAiOjE4MDg4NDAxNzcsInN1YiI6IkdVRVNUIiwicm9sZSI6IkdVRVNUIiwidGVuYW50IjoiY29tIiwidHlwZSI6IkFDQ0VTUyIsImtleVZlcnNpb24iOiJmMjI3MGU4OS1iOGJjLTQ1ODAtOTA2MC01OTBmMTNiYjkyMjEiLCJkZXZpY2VUeXBlIjoiYW5kcm9pZEFwcCIsImV4cFJlZnJlc2giOiIyMDI3LTA0LTI3VDE1OjM2OjE3LjM2NloiLCJqdGkiOiI2MDg4NDA5Mi04NzE2LTQ2Y2EtYTllMi0wMWQ3MmNiYzVhMjYiLCJpc3MiOiJhdXRoLnJlZHRlY2xhYi5jb20iLCJpYXQiOjE3NzcyODMyMzd9.bFY3-kIZ9ZMnocQdyMHlTpYE9YxA0n-TiiI9ed0NamtEsvEkRahXOoZbGjGKx8ILxH7gU2sBiAiyI5oVjqCDooYlUon1UdD9ZN6Ario_ewVaPTH1CRtlXkZrA-v4eMBGrP_AMh6fmr6dH0S3vLnjW5g_S4j8t0K2KYesWgWty1yXpWL8dZIVXKLgiH_CMVOwQWdjP7JyOwGS0TTzz-IyHRB0ThiD4gOi-wllidtMNX21W8XuD6lOLbaaoVkUuDtbxLxX6hq7RoPV_3FNcQK6h43VxVWvjdDVnhtDKvzqtab0IAdiSVEhMel4lm_jaVjDp3w42ChTCaGe039nt90iE8cCdefUGVlOTQk3o0R4yurinsl8ESUcBvIKJFnFNgIQuTL5_598lj8TDJcmFLOYqvtJoNjH7dLAxERbcZ9ADx0A-doc8d8N_TVhpGS22-3tVkry_2_X8f4uR9_lVI9Z20S2LCUy-NevFHcBzVSEwnJ0aWMMF1EHbHAvWOp0X-VI"
}
```

================================================================================

### Endpoint: POST https://api.sa-tech.de/auth/v2/com/register
**Status**: 201
#### Request
```json
{"dateOfBirth":"1998-04-15","email":"deepanshusinghdigitalheroes@gmail.com","firstName":"Deepanshu","lastName":"Singh","newsletterAccepted":false,"password":"Facebook@ds12,","preferredLanguage":"de","registrationOrigin":"app","salutation":"mr","tosAccepted":true}
```
#### Response
```json
{
  "tokenType": "bearer",
  "token": "eyJraWQiOiJmMjI3MGU4OS1iOGJjLTQ1ODAtOTA2MC01OTBmMTNiYjkyMjEiLCJhbGciOiJSUzM4NCJ9.eyJleHAiOjE4MDg4NDAxNzcsInN1YiI6IjI1MTQ2Mjk4NDgiLCJyb2xlIjoiUkVHSVNURVJFRCIsInRlbmFudCI6ImNvbSIsInR5cGUiOiJBQ0NFU1MiLCJrZXlWZXJzaW9uIjoiZjIyNzBlODktYjhiYy00NTgwLTkwNjAtNTkwZjEzYmI5MjIxIiwiZGV2aWNlVHlwZSI6ImFuZHJvaWRBcHAiLCJleHBSZWZyZXNoIjoiMjAyNi0wNC0yN1QxMDowMjoxNy45NDRaIiwiZXhwU2Vuc2l0aXZlIjoiMjAyNy0wNC0yN1QxNTozNjoxNy45NDRaIiwianRpIjoiNjA4ODQwOTItODcxNi00NmNhLWE5ZTItMDFkNzJjYmM1YTI2IiwiaXNzIjoiYXV0aC5yZWR0ZWNsYWIuY29tIiwiaWF0IjoxNzc3MjgzMjM3fQ.QIevGI0VQ0a42BV_NNBSKvNcBiEsDE-i_xiGldChkW0bPUUMdTlxzZ8zCPXoFT9XI1JZ3js3g7pirIrC-Zw_2PrcSUGKpj61DF-JqvYmK4WUh6SqKpO2xeboUIxQ3V_hEXy7DbwBCflIzoXW0HChaJDUmafm_W44luyLKqDcCCvv5vjTP2g8WnVDhpIwxsZdIpOMr2upN6Niq8Ff3zdmHLdRFlfNooF2Zehzgc-5n-43kKQ0hC4ZjCMB36Yby_zgFMXhCrXT_pRh4hzJPffC3O2FiXK3K4aKEgjYXeaSeus_banSJWE4pxAysSOKPtvCTf5Xu5GW0c8iXf9WtpSqYDMOMCTWKJTzAnoKI6pXlARRw558M-vJn3_zNmxC9HwbblCfng1BUOIKijxN2VyAO8Arg759INct-VcpFeARPblKyhbx0qLNGShHkb15Jb54_lW3MW_bONt_Rw6iXHawkUThU81pAMnR1MRwXS3SpHSfbs0kYXRfLGMU6tg9ZJRu"
}
```

================================================================================

### Endpoint: GET https://api.sa-tech.de/account/v2/com/de/user
**Status**: 200
#### Request
*No Body*
#### Response
```json
{
  "billingAddress": {},
  "customerNumber": "2514629848",
  "dateOfBirth": "1998-04-15",
  "email": "deepanshusinghdigitalheroes@gmail.com",
  "firstName": "Deepanshu",
  "isEavCustomer": false,
  "lastName": "Singh",
  "mailingSubscriptions": [],
  "redPointsMembership": "NO_MEMBER",
  "salutation": "mr",
  "totalOrders": 0,
  "totalAppOrders": 0,
  "totalERxOrders": 0,
  "totalNowOrders": 0,
  "eligibleCredit": 0,
  "customerType": "customer",
  "emailValidated": false
}
```

================================================================================

### Endpoint: GET https://api.sa-tech.de/de/cart/v3/com?purgeMessages=false&nowZipCode=&distributionType=none&isNowSelected=false
**Status**: 200
#### Request
*No Body*
#### Response
```json
{
  "acceptedVouchersCodes": [],
  "rxBonusTotal": 0,
  "rxBonusDiscount": 0,
  "rxBonusToAccount": 0,
  "redPointsTotal": 0,
  "redPointsTotalAmount": 0,
  "shippingCostTotal": 0,
  "shippingDetail": [],
  "id": "69ef30a76efd12dad6494fcc",
  "collectiveOrder": false,
  "created": "2026-04-27T09:47:19.625Z",
  "lastUpdated": "2026-04-27T09:47:19.676Z",
  "currency": "EUR",
  "customerId": "60884092-8716-46ca-a9e2-01d72cbc5a26",
  "tenant": "com",
  "totalAmount": 0,
  "subAmount": 0,
  "subAmountWithLineDiscounts": 0,
  "discountAmountTotal": 0,
  "messages": [],
  "sellerGroups": [],
  "redPointsPossibleDiscounts": [],
  "applicableCredit": 0,
  "prescriptionFollows": false,
  "redPointsRegistrationStatus": "",
  "redeemableRedPoints": 0,
  "totalAmountWithoutShipping": 0,
  "totalAppliedDiscounts": 0,
  "totalAppliedDiscountsWithoutLineDiscounts": 0,
  "totalAppliedVouchersDiscount": 0,
  "totalAppliedRedPointsDiscount": 0,
  "totalCreditAndPublicBonus": 0,
  "overdrafts": [],
  "maxDosageDetails": [],
  "promotionInformation": []
}
```

================================================================================

### Endpoint: GET https://api.sa-tech.de/account/v2/com/de/user
**Status**: 200
#### Request
*No Body*
#### Response
```json
{
  "billingAddress": {},
  "customerNumber": "2514629848",
  "dateOfBirth": "1998-04-15",
  "email": "deepanshusinghdigitalheroes@gmail.com",
  "firstName": "Deepanshu",
  "isEavCustomer": false,
  "lastName": "Singh",
  "mailingSubscriptions": [],
  "redPointsMembership": "NO_MEMBER",
  "salutation": "mr",
  "totalOrders": 0,
  "totalAppOrders": 0,
  "totalERxOrders": 0,
  "totalNowOrders": 0,
  "eligibleCredit": 0,
  "customerType": "customer",
  "emailValidated": false
}
```

================================================================================

### Endpoint: GET https://api.sa-tech.de/account/v2/com/de/user
**Status**: 200
#### Request
*No Body*
#### Response
```json
{
  "billingAddress": {},
  "customerNumber": "2514629848",
  "dateOfBirth": "1998-04-15",
  "email": "deepanshusinghdigitalheroes@gmail.com",
  "firstName": "Deepanshu",
  "isEavCustomer": false,
  "lastName": "Singh",
  "mailingSubscriptions": [],
  "redPointsMembership": "NO_MEMBER",
  "salutation": "mr",
  "totalOrders": 0,
  "totalAppOrders": 0,
  "totalERxOrders": 0,
  "totalNowOrders": 0,
  "eligibleCredit": 0,
  "customerType": "customer",
  "emailValidated": false
}
```

================================================================================

### Endpoint: GET https://api.sa-tech.de/mobileaccount/v1/com/pushNotificationsConfiguration/DE.2514629848
**Status**: 200
#### Request
*No Body*
#### Response
```json
{}
```

================================================================================

### Endpoint: GET https://api.sa-tech.de/mobileaccount/v1/com/appcoupons/DE.2514629848
**Status**: 200
#### Request
*No Body*
#### Response
```json
[
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_linola_2604",
    "type": "percentage",
    "amount": 20,
    "target": "brand",
    "targetName": "Linola",
    "includeList": [
      "10017585",
      "10339828",
      "A8001371",
      "14445846",
      "08768976",
      "17628582",
      "05484296",
      "17556836",
      "15607297",
      "00683565",
      "18294982",
      "04024782",
      "09221091",
      "11657594",
      "14318823",
      "04412573",
      "11230743",
      "06797904",
      "06170944",
      "18092528",
      "08110133",
      "16002840",
      "11230720",
      "00979113",
      "04222849",
      "06170938",
      "08112742",
      "11637166",
      "10102138",
      "04222832",
      "19264954",
      "08106526",
      "08119822",
      "08119835",
      "08119877",
      "08119901",
      "08119913",
      "08119917",
      "08119925",
      "08119944",
      "08120014",
      "08120166"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/linola.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 390,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_eucerin_2604",
    "type": "percentage",
    "amount": 20,
    "target": "brand",
    "targetName": "Eucerin",
    "includeList": [
      "00074458",
      "00601656",
      "00802461",
      "00921421",
      "01171175",
      "01552397",
      "02398082",
      "02398107",
      "02398780",
      "03709816",
      "03815725",
      "04668723",
      "07415483",
      "07608420",
      "08076084",
      "08104705",
      "08104749",
      "08104752",
      "08106854",
      "08106855",
      "08106857",
      "08106858",
      "08106859",
      "08106861",
      "08106960",
      "08106962",
      "08106963",
      "08106964",
      "08106965",
      "08107429",
      "08108292",
      "08108293",
      "08108299",
      "08108300",
      "08108303",
      "08108304",
      "08108307",
      "08108309",
      "08108311",
      "08108313",
      "08108314",
      "08111426",
      "08111427",
      "08112731",
      "08112732",
      "08112733",
      "08112735",
      "08112738",
      "08112747",
      "08114663",
      "08114664",
      "08114665",
      "08114666",
      "08114667",
      "08114780",
      "08115101",
      "08115102",
      "08115103",
      "08115104",
      "08115105",
      "08115106",
      "08115108",
      "08115109",
      "08115110",
      "08115111",
      "08115113",
      "08115114",
      "08115115",
      "08115116",
      "08115117",
      "08115118",
      "08115119",
      "08115120",
      "08115989",
      "08115990",
      "08115991",
      "08115992",
      "08115993",
      "08115994",
      "08115995",
      "08115996",
      "08115998",
      "08115999",
      "08116000",
      "08116001",
      "08116002",
      "08116003",
      "08116004",
      "08116005",
      "08116006",
      "08116007",
      "08116008",
      "08116009",
      "08116010",
      "08116011",
      "08116012",
      "08116013",
      "08116014",
      "08116015",
      "08116016",
      "08116017",
      "08116018",
      "08116019",
      "08116020",
      "08116021",
      "08116022",
      "08116023",
      "08116024",
      "08116025",
      "08116026",
      "08116027",
      "08116028",
      "08119852",
      "08119879",
      "08119899",
      "08119903",
      "08119905",
      "08119909",
      "08119910",
      "08119918",
      "08119927",
      "08119939",
      "08119952",
      "08119958",
      "08119960",
      "08119963",
      "08119969",
      "08119980",
      "08119982",
      "08119984",
      "08119998",
      "08119999",
      "08120025",
      "08120035",
      "08120055",
      "08120100",
      "08120103",
      "08120224",
      "08120264",
      "08454700",
      "08454746",
      "08454775",
      "08454781",
      "08651665",
      "08796286",
      "09284370",
      "09289456",
      "09508059",
      "09508065",
      "09508071",
      "09508088",
      "09508094",
      "09508102",
      "10268643",
      "10268666",
      "10268672",
      "10268689",
      "10268695",
      "10779409",
      "10832658",
      "10832664",
      "10961350",
      "10961396",
      "11321322",
      "11652958",
      "11652964",
      "11677993",
      "11678001",
      "11678024",
      "11678047",
      "11678099",
      "11678142",
      "11678159",
      "11692900",
      "12441459",
      "13167925",
      "13235762",
      "13827971",
      "13827988",
      "13889015",
      "13889021",
      "13889038",
      "13889044",
      "13889073",
      "13889096",
      "13889133",
      "13889156",
      "13889179",
      "13889185",
      "13889191",
      "13889216",
      "13889222",
      "13889239",
      "13889251",
      "13889268",
      "13929074",
      "14163881",
      "14163898",
      "14163912",
      "14163929",
      "14179451",
      "14215997",
      "14216005",
      "14292845",
      "14297073",
      "15205972",
      "15210513",
      "15257408",
      "15294332",
      "15294349",
      "15562560",
      "15581586",
      "15623422",
      "15623451",
      "16015570",
      "16015587",
      "16143115",
      "16143121",
      "16143138",
      "16154604",
      "16154610",
      "16236673",
      "16502614",
      "16510884",
      "16585528",
      "16756504",
      "16807294",
      "16871352",
      "16887494",
      "16887502",
      "16901337",
      "16907127",
      "17200737",
      "17510722",
      "17510739",
      "17510751",
      "17553453",
      "17553565",
      "17674903",
      "17674926",
      "17882978",
      "17929757",
      "18099921",
      "18110226",
      "18110232",
      "18173273",
      "18173296",
      "18201503",
      "18222089",
      "18222103",
      "18487735",
      "18487741",
      "19116202",
      "19166884",
      "19169919",
      "19169931",
      "19173499",
      "19343317",
      "19343346",
      "19358514",
      "19460767",
      "19460773",
      "19490308",
      "19490314",
      "19645188",
      "19708405",
      "19708411",
      "19708434",
      "19708440",
      "19723913",
      "19723936",
      "19723942",
      "19723959",
      "19729809",
      "19729815",
      "19729821",
      "19729838",
      "19729844",
      "19729850",
      "19729867",
      "19729873",
      "19729896",
      "19729904",
      "19729910",
      "20044560",
      "20091051",
      "20091068",
      "A8000538",
      "A8000543",
      "A8000554",
      "A8001094",
      "A8001104",
      "A8001128",
      "A8001146",
      "A8001236",
      "A8001448",
      "A8001501",
      "A8001600",
      "A8001602",
      "A8002104",
      "A8002121"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/eucerin.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 350,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_otc_blase_2604",
    "type": "percentage",
    "amount": 20,
    "target": "category",
    "targetName": "Blasengesundheit & Harnwegserkrankungen",
    "includeList": [
      "07114824",
      "07126744",
      "16884923",
      "16884952",
      "07152960",
      "16151735",
      "16151764",
      "16151770",
      "08107552",
      "10011915",
      "10011921",
      "10011938",
      "08110411",
      "00795287",
      "08105913",
      "08114207",
      "01499852",
      "01499898",
      "03046327",
      "08112392",
      "19339043",
      "08114607",
      "10318105",
      "10318111",
      "10318128",
      "08105795",
      "04976494",
      "04976502",
      "00424935",
      "00266608",
      "00266614",
      "00301233",
      "08105796",
      "01300721",
      "01300750"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/moodbildblase.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 300,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-16",
    "endDate": "2026-05-16",
    "code": "appcoupon_sports_magnesium_260",
    "type": "percentage",
    "amount": 20,
    "target": "category",
    "targetName": "Magnesium f\u00fcr Sportler",
    "includeList": [
      "5852222",
      "5132634",
      "5852191",
      "5133036",
      "16018640",
      "8107485",
      "CH90001428",
      "CH90001002",
      "8107491",
      "8107492",
      "12502505",
      "10793160",
      "8114635",
      "11562267",
      "A2682765",
      "2597700",
      "2833709",
      "19373235",
      "19068897",
      "8102063",
      "8111611",
      "19361404",
      "8104861",
      "16231871",
      "A2745709"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/moodbildmagnesium.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 16.05.2026. Can be combined with other coupons.",
    "priority": 100,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_nagelpilz_2604",
    "type": "percentage",
    "amount": 20,
    "target": "product",
    "targetName": "Nagelpilz",
    "includeList": [
      "00619053",
      "08109893",
      "08079612",
      "15371297",
      "08109237",
      "08109238",
      "08108549",
      "08907113",
      "02247667",
      "08907142",
      "18762911",
      "03963242",
      "11013388",
      "09091228",
      "09091234",
      "08112967",
      "08112966",
      "09199173",
      "09199196",
      "08109799"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/moodbildnagelpilz.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 100,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_vet_pflege_2604",
    "type": "percentage",
    "amount": 20,
    "target": "category",
    "targetName": "Haut-, Fell- & Hufpflege f\u00fcr Ihr Pferd",
    "includeList": [
      "14033492",
      "17148327",
      "16361912",
      "14033500",
      "08111104",
      "17148310",
      "08108538",
      "18378466",
      "08111103",
      "03674779",
      "04976301",
      "08114192",
      "11870164",
      "08114193",
      "01316863",
      "11870170",
      "08055704",
      "11870141",
      "12647592",
      "11870158",
      "08055779",
      "11332797",
      "19444745",
      "08111387",
      "18778645",
      "17835157",
      "08111993",
      "18132127",
      "08111994",
      "08114185",
      "19444722",
      "08111996",
      "17835200",
      "05702043",
      "18778622",
      "02488454",
      "13946977",
      "17167342",
      "08026499",
      "18378489",
      "17148333",
      "19444739",
      "A5457477",
      "01170419",
      "08111989",
      "18378526",
      "08111443",
      "18444393",
      "A5681387",
      "19444716",
      "19444691",
      "02780002",
      "06715651",
      "08111990",
      "A5747028",
      "18378503",
      "17198147",
      "08590952",
      "17304247",
      "10313929",
      "08111101",
      "16242403",
      "08111102",
      "08114181",
      "17304253",
      "16577492",
      "17198093",
      "08111100",
      "17591494",
      "17198070",
      "18132104",
      "01402918",
      "17850180",
      "09670966",
      "19196968",
      "11339658",
      "08100053",
      "08023503",
      "08111428",
      "A5685764",
      "19174932",
      "18784918",
      "07734573",
      "04902484",
      "A5463489",
      "16361817",
      "A5348647",
      "08108814",
      "17537106",
      "17835246"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/moodbildpferd.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 100,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_bigaia_2604",
    "type": "percentage",
    "amount": 20,
    "target": "brand",
    "targetName": "BiGaia",
    "includeList": [
      "20038217",
      "20038252",
      "19926303",
      "19926332",
      "19926361",
      "19926355",
      "20038246",
      "20038223"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/bigaia.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 100,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_elasten_2604",
    "type": "percentage",
    "amount": 20,
    "target": "brand",
    "targetName": "Elasten",
    "includeList": [
      "10048806",
      "15233744",
      "08108289",
      "16929956"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/elasten.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 100,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_sports_optimum_2604",
    "type": "percentage",
    "amount": 15,
    "target": "brand",
    "targetName": "Optimum Nutrition",
    "includeList": [
      "08101683",
      "08105410",
      "08101730",
      "08101680",
      "08101684",
      "08101749",
      "08101682",
      "08101698",
      "08105411",
      "08101735",
      "08101733",
      "08101681",
      "08110993",
      "08101723",
      "08110989",
      "08101747",
      "08101685",
      "08101703",
      "08101689",
      "08111000"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/optimum.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 100,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_weleda_2604",
    "type": "percentage",
    "amount": 15,
    "target": "brand",
    "targetName": "Hom\u00f6opathische Weleda",
    "includeList": [
      "03141362",
      "18022775",
      "00761710",
      "17935232",
      "17935195",
      "03933100",
      "00230065",
      "03643112",
      "00171138",
      "17977466",
      "01572856",
      "08110017",
      "01572106",
      "00460612",
      "03933092",
      "06888067",
      "00171121",
      "03141416",
      "08113491",
      "03141451",
      "17935226",
      "06888050",
      "06888044",
      "06888038",
      "01589928",
      "08113510",
      "06059282",
      "06059276",
      "05486674",
      "00442755",
      "03205659",
      "15432917",
      "08109686",
      "02591904",
      "01631441",
      "01390138"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/weleda.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 100,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_redcare_junior_2604",
    "type": "percentage",
    "amount": 25,
    "target": "brand",
    "targetName": "Redcare Junior & Derma ",
    "includeList": [
      "08116055",
      "08116063",
      "08116065",
      "08116064",
      "08116066",
      "08116056",
      "08116057",
      "08116058",
      "08116060",
      "08116062",
      "08116068",
      "08116061",
      "08116059",
      "08107259",
      "17422202",
      "08107232",
      "08110870",
      "16599619",
      "18036010",
      "08109759",
      "08109771",
      "18067387",
      "08110095",
      "18036027",
      "08110883",
      "08107262",
      "17521430",
      "08110894",
      "08111561",
      "19176859",
      "08111961",
      "20015506",
      "19822288",
      "19815207",
      "08114284",
      "20024528",
      "20024534",
      "19482183",
      "08113260",
      "08113261",
      "19511915",
      "08109465",
      "08110882",
      "18158954",
      "08111883",
      "18798429",
      "08112286",
      "19375866",
      "08112291",
      "08112292",
      "19301000",
      "08112287",
      "19854710",
      "19854673",
      "19854696",
      "19854667",
      "19854704",
      "08107255",
      "08110088",
      "17386127",
      "08110874",
      "17284148",
      "08107252",
      "19769418",
      "08114659",
      "20032404",
      "20032373",
      "20032396",
      "08115931"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/Redcare.jpg",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 100,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_rapunzel_2604",
    "type": "percentage",
    "amount": 20,
    "target": "brand",
    "targetName": "Rapunzel",
    "includeList": [
      "08107474",
      "08101543",
      "A8000848",
      "08107490",
      "08110536",
      "08109224",
      "08107401",
      "08110543",
      "A8000838",
      "08103837",
      "08101538",
      "08101520",
      "08104028",
      "08113442",
      "08101533",
      "08113443",
      "08110534",
      "08101546",
      "08101545",
      "08101485",
      "08101556",
      "08110360",
      "08107670",
      "08113444",
      "08105188",
      "08101532",
      "08104138",
      "08101488",
      "08101499",
      "08101560",
      "08109225",
      "08101539",
      "08101489",
      "08110361",
      "08101487",
      "08113448",
      "08101479",
      "08101544",
      "08103841",
      "08101535",
      "08101516",
      "08104009",
      "08101522",
      "08112803",
      "08101528",
      "08101542",
      "08101536",
      "08113454",
      "08101564",
      "08112825",
      "08101496",
      "08113451",
      "08112824",
      "08109778",
      "08113447",
      "08101519",
      "08113460",
      "08103434",
      "08101549",
      "08113446",
      "08107744",
      "08104010",
      "08103840",
      "08101478",
      "08101506",
      "08101507",
      "08112815",
      "08113445",
      "08101531",
      "08101529",
      "08111877",
      "08104004",
      "08101523",
      "08104140",
      "08101498",
      "08101521",
      "08113449",
      "08104137",
      "08113455",
      "08107733",
      "08101476",
      "08101495",
      "08101491",
      "08109223",
      "08101565",
      "08101552",
      "08101557",
      "08104136",
      "08101483",
      "08104007",
      "08101475",
      "08101513",
      "08107680",
      "08110535",
      "08101484",
      "08104006",
      "08101537",
      "08101561",
      "08104139",
      "08104011",
      "08113184",
      "08113461",
      "08101486",
      "08113456",
      "08101477",
      "08113452",
      "08112797",
      "08112813",
      "08101492",
      "08112826"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/rapunzel.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 100,
    "maxRedemptions": 1
  },
  {
    "activated": false,
    "public": true,
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "code": "appcoupon_armolipid_2604",
    "type": "percentage",
    "amount": 20,
    "target": "brand",
    "targetName": "Armolipid",
    "includeList": [
      "12477635",
      "01971881",
      "18498733",
      "08110079",
      "01926188",
      "18498727",
      "08113233"
    ],
    "imageUrl": "https://static.shop-apotheke.com/coupon-images/armolipid.png",
    "legalText": "This coupon is valid once per customer and cannot be combined with other promotions. Cash payment excluded. Valid until 30.04.2026. Can be combined with other coupons.",
    "priority": 100,
    "maxRedemptions": 1
  }
]
```

================================================================================

### Endpoint: GET https://api.sa-tech.de/session/v1/com/erx-session-status/2514629848
**Status**: 404
#### Request
*No Body*
#### Response
```json
{
  "statusCode": 404,
  "error": "Not Found",
  "message": "customer-data-service.error.not_found"
}
```

================================================================================

### Endpoint: GET https://api.sae-conversational.com/userlike-operators?language=de&tenant=erx
**Status**: 200
#### Request
*No Body*
#### Response
```json
[
  {
    "id": 223573,
    "displayName": "Riswana Ali",
    "name": "Riswana Ali",
    "active": true,
    "lang": "de",
    "operatorGroup": "App_DE_AT_eRX_support",
    "isAvailable": true,
    "skills": [
      {
        "id": 586227,
        "text": "Android / IOS NFC Chat",
        "name": "App_DE_AT_eRX"
      }
    ]
  },
  {
    "id": 223880,
    "displayName": "Philipp Dziachan",
    "name": "Philipp Dziachan",
    "active": true,
    "lang": "de",
    "operatorGroup": "App_DE_AT_eRX_support",
    "isAvailable": true,
    "skills": [
      {
        "id": 586227,
        "text": "Android / IOS NFC Chat",
        "name": "App_DE_AT_eRX"
      }
    ]
  },
  {
    "id": 224361,
    "displayName": "Verena Gablenz",
    "name": "Verena Gablenz",
    "active": true,
    "lang": "de",
    "operatorGroup": "App_DE_AT_eRX_support",
    "isAvailable": true,
    "skills": [
      {
        "id": 55450,
        "text": "Speaks German",
        "name": "German"
      },
      {
        "id": 586227,
        "text": "Android / IOS NFC Chat",
        "name": "App_DE_AT_eRX"
      }
    ]
  },
  {
    "id": 223883,
    "displayName": "Lisa Schr\u00f6der",
    "name": "Lisa Schr\u00f6der",
    "active": true,
    "lang": "de",
    "operatorGroup": "App_DE_AT_eRX_support",
    "isAvailable": true,
    "skills": []
  }
]
```

================================================================================

### Endpoint: POST https://api.sa-tech.de/customer/v1/com/mfa/2514629848/phone-verification/request
**Status**: 204
#### Request
```json
{"phoneNumber":"+491765550123"}
```
#### Response
```json

```

================================================================================

### Endpoint: POST https://api.sa-tech.de/customer/v1/com/mfa/2514629848/phone-verification/confirmation
**Status**: 400
#### Request
```json
{"code":"222222"}
```
#### Response
```json
{
  "statusCode": 400,
  "error": "Bad Request",
  "message": "erx.phone_verification.password_rejected"
}
```

================================================================================


--- Unique Endpoints ---
GET http://android.httptoolkit.tech/config
GET https://aggregator.service.usercentrics.eu/aggregate/en
GET https://api.instabug.com/api/sdk/v3/application_categories
GET https://api.instabug.com/api/sdk/v3/features
GET https://api.instabug.com/api/sdk/v3/first_seen
GET https://api.leanplum.com/api
GET https://api.sa-tech.de/account/v2/com/de/user
GET https://api.sa-tech.de/auth/v1/com/login/guest
GET https://api.sa-tech.de/crosssellers/v2/com/de
GET https://api.sa-tech.de/customers/traits/DE.2514629848
GET https://api.sa-tech.de/de/app-config/v1
GET https://api.sa-tech.de/de/cart/v3/com
GET https://api.sa-tech.de/de/cart/v3/com/minicart
GET https://api.sa-tech.de/mobileaccount/v1/com/appcoupons/DE.2514629848
GET https://api.sa-tech.de/mobileaccount/v1/com/pushNotificationsConfiguration/DE.2514629848
GET https://api.sa-tech.de/session/v1/com/erx-session-status/2514629848
GET https://api.sae-conversational.com/userlike-operators
GET https://api.usercentrics.eu/settings/m7vK-rc0i/latest/en.json
GET https://api.usercentrics.eu/settings/m7vK-rc0i/latest/languages.json
GET https://api.usercentrics.eu/translations/translations-en.json
GET https://app-measurement.com/config/app/1:129759020696:android:04025d0e7049144b
GET https://app.usercentrics.eu/session/1px.png
GET https://appassets.androidplatform.net/favicon.ico
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjAwMTI3X0RFXzIwMjZfMDE3NF9MT1VfREVfMDAyNS5qcGc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjAyNTA1MDgtQ09NLUJlaWVyc2RvcmYtUHVzaE5vdGlmaWNhdGlvbi02NDB4MzIwLmpwZw==
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjUxMTI3LUNPTS1SYXRpb3BoYXJtU3lub2Zlbi1BcHBIZXJvQmFubmVyLTEwMDB4NTAwLmpwZw==
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjUxMjE2LWNvbS1lcmV6ZXB0LTEwcmV6ZXB0LTEwMDB4NTAwICgxKS5qcGc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjYwMTA0LWNvbS1zb25uZS0xMDAweDUwMC5qcGc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjYwMTI3LUNPTS1Eb2xvcm1pbkV4dHJhLUFwcFNsaWRlci0xMDAweDUwMC5qcGc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjYwMTIxLWVyc3Rlcy1lcmV6ZXB0LTY0OHgxMDQzLmpwZw==
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjYwMTIyLUNPTS1CYXllclZpdGFsLUFzcGlyaW5Db2xkLUFwcFNsaWRlci0xMDAweDUwMC5qcGc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjYwMzEzLWNvbS1rcmFmdC1hdXNkYXVlci0xMDAweDUwMC5qcGc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjYwMzEzLWNvbS1tYWdlbi1kYXJtLTEwMDB4NTAwLmpwZw==
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjYwMzEzLWNvbS1tYWdlbi1kYXJtLTEwMDB4NTAwMS5qcGc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/MjYwMzI0LWNvbS1vc3Rlcm4tcmVkcG9pbnRzLTEwMDB4NTAwLTIuanBn
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/QXBwLVNsaWRlci0xMDAweDUwMC12aXRhbWluLWQzLnBuZw==
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/REVfMjAyNl8wMDE2X0FOR19ERV8wMDA4LUFuZ2VsaW5pLUFwcHNsaWRlci5qcGc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/REVfMjAyNl8wMDMwX0JFSV9ERV8wMDc1X0pTICgxKS5qcGc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/REVfMjAyNl8wMTc3X01FRF9ERV8wMDI3IC0gTWVkaWNlIC0gTWVkaXRvbnNpbiBFeHRyYWt0ICgxKS5qcGc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/SWNvbi5wbmc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/Y29tLUFwcC1CZXN0ZWxsdW5nLUFwcC0xMDAweDUwMC12Mi5qcGc=
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/aWNfYmFubmVyXzYucG5n
GET https://assets.prod.leanplum.com/app_GzbWqCw7ctWuiDOwUOvgxVjmxRnAE1dG352Ru2RkNGo/aWNfYmFubmVyXzkucG5n
GET https://cdn.shop-apotheke.com/images/D01/126/111/D01126111-p1.jpg
GET https://cdn.shop-apotheke.com/images/D10/019/621/D10019621-p1.jpg
GET https://connectivitycheck.gstatic.com/generate_204
GET https://digital-cloud.apis.medallia.eu/mobileSDK/v1/configuration
GET https://edge.eu1.fullstory.com/s/fs.js
GET https://edge.eu1.fullstory.com/s/settings/o-RPS-eu1/v1/mobile
GET https://firebase-settings.crashlytics.com/spi/v2/platforms/android/gmp/1%3A129759020696%3Aandroid%3A04025d0e7049144b/settings
GET https://firebase-settings.crashlytics.com/spi/v2/platforms/android/gmp/1:129759020696:android:04025d0e7049144b/settings
GET https://jsi4pf.cdn-settings.appsflyersdk.com/android/v2/cdfc956909e7a4ed986950723ce2efed2562b5f388d55762ea5c64281f1b44bf/settings
GET https://jsi4pf.gcdsdk.appsflyersdk.com/install_data/v5.0/shop.shop_apotheke.com.shopapotheke
GET https://ota-bundles.lokalise.com/168777/6087199262f4d6b24b8679.24668444/bundles/a1ac4e7e-6fb7-4f09-96f9-7873c09f719f
GET https://ota.lokalise.com/v2.0/android/
GET https://play.google.com/store/apps/details
GET https://play.googleapis.com/play/log/timestamp
GET https://resources.digital-cloud.medallia.eu/md-form/mobileAndroid/1.23.1/index.html
GET https://resources.digital-cloud.medallia.eu/resources/sdk/staticLocalization.json
GET https://resources.digital-cloud.medallia.eu/wdceu/136700/resources/image/1659347388019_Redcare_logo_-_Small.png
GET https://resources.digital-cloud.medallia.eu/wdceu/136700/resources/image/1699257572482_ShopApotheke_New_200px.png
GET https://resources.digital-cloud.medallia.eu/wdceu/136700/resources/image/1701072334908_Redcare_CH_logo_-_Small.png
GET https://resources.digital-cloud.medallia.eu/wdceu/136700/resources/image/1701245831798_Redcare_FR_logo_-_Small.png
GET https://resources.digital-cloud.medallia.eu/wdceu/136700/resources/image/1721034546903_Farmaline_logo_-_small.png
GET https://resources.digital-cloud.medallia.eu/websites/136700/sdk/localization-1775569188230.zip
GET https://static.shop-apotheke.com/coupon-images/eucerin.png
GET https://static.shop-apotheke.com/coupon-images/linola.png
GET https://static.shop-apotheke.com/media/content/placeholder.png
GET https://static.shop-apotheke.com/media/js/shopmonitor.js
GET https://static.shop-apotheke.com/media/medallia/Shop_apotheke_Redcare_v4.css
GET https://storage.googleapis.com/leanplum_resources_public/lp_public_image-interstitial-2.html
GET https://www.econda-monitor.de/l/000016f3/t/496c2984-7951-4ed2-b556-1bdfdd0856c4
GET https://www.googletagmanager.com/gtm.js
POST http://c.whatsapp.net/chat
POST https://android.apis.google.com/c2dm/register3
POST https://api.leanplum.com/api
POST https://api.sa-tech.de/auth/v2/com/register
POST https://api.sa-tech.de/customer/v1/com/mfa/2514629848/phone-verification/confirmation
POST https://api.sa-tech.de/customer/v1/com/mfa/2514629848/phone-verification/request
POST https://api.sa-tech.de/nfc-health-card-position/api/v1/nfc-position
POST https://api.sae.systems/rma/api/v1/d
POST https://api.sae.systems/rma/api/v1/udb/sync
POST https://app-measurement.com/a
POST https://consent-api.service.consent.usercentrics.eu/consent/ua/3
POST https://digital-cloud.apis.medallia.eu/mobileSDK/v1/accessToken
POST https://eu1.clevertap-prod.com/a1
POST https://firebaseinstallations.googleapis.com/v1/projects/shop-apotheke-app-ios/installations
POST https://firebaselogging-pa.googleapis.com/v1/firelog/legacy/batchlog
POST https://firebaseremoteconfig.googleapis.com/v1/projects/129759020696/namespaces/fireperf:fetch
POST https://inbox.google.com/sync/i/fd
POST https://inbox.google.com/sync/i/s
POST https://jsi4pf.conversions.appsflyersdk.com/api/v6.18/androidevent
POST https://jsi4pf.dlsdk.appsflyersdk.com/v1.0/android/shop.shop_apotheke.com.shopapotheke
POST https://jsi4pf.inapps.appsflyersdk.com/api/v6.18/androidevent
POST https://jsi4pf.pia.appsflyersdk.com/api/v1.0/pia-android-event
POST https://jsi4pf.register.appsflyersdk.com/api/v6.18/androidevent
POST https://listener-eu.logz.io:8071/
POST https://mr.eu1.fullstory.com/rec/bundle/v2
POST https://mr.eu1.fullstory.com/rec/newResources
POST https://mr.eu1.fullstory.com/rec/page
POST https://play-fe.googleapis.com/fdfe/apps/contentSync
POST https://play-fe.googleapis.com/fdfe/integrity
POST https://play-fe.googleapis.com/fdfe/intermediateIntegrity
POST https://play.googleapis.com/play/log
POST https://taskassist-pa.googleapis.com/v2/taskassist:compose
POST https://uct.service.usercentrics.eu/uct
