# Sanjay Kumar Yadav | Personal GIS & Remote Sensing Portfolio

A static personal portfolio documenting professional experience, geospatial and data management skills, formal education, selected training and analytical focus areas.

## Pages

- `docs/index.html` - personal introduction and analytical focus
- `docs/about.html` - career timeline and education from the latest CV
- `docs/expertise.html` - GIS, 12 agricultural indices (full names only), imagery capabilities, UAV data analysis and elevation analysis
- `docs/projects.html` - portfolio areas: multispectral imagery, terrain models, drone imagery and spatial field-data checks
- `docs/gallery.html` - clearly labeled illustrative GIS/dashboard/forms/web examples
- `docs/credentials.html` - training certificates and qualifications
- `docs/contact.html` - professional contact details

The old `docs/solutions.html` path redirects to `docs/gallery.html` to preserve existing bookmarks. This is a **personal portfolio**, not a commercial services catalog.

## Terminology and analytical scope

- Sentinel-2: MultiSpectral Instrument (MSI).
- Landsat 8: Operational Land Imager (OLI).
- Landsat 9: Operational Land Imager 2 (OLI-2).
- DEM: Digital Elevation Model; DTM: Digital Terrain Model; DSM: Digital Surface Model.
- UAV: Unmanned Aerial Vehicle (drone) imagery data analysis.

Red-edge-specific indices depend on Sentinel-2 bands not provided by Landsat 8/9 OLI-family imagery. Drone-derived Near-Infrared indices require an appropriate multispectral sensor, not RGB photos alone.

The technical scope is a portfolio of described skills and methods. Illustrations are not represented as client-owned project results, verified accuracy figures or confidential datasets.

## Preview locally

```sh
python3 -m http.server 8000 --directory docs
```

Open `http://localhost:8000/` to inspect the static pages.

## Site maintenance

Update career details from the latest CV, preserve privacy of field records, keep sitemap and canonical URLs consistent, and verify responsive navigation before publishing.
