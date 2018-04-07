from flask_assets import Bundle

app_css = Bundle('app.scss', filters='scss', output='styles/app.css')

app_js = Bundle('app.js', filters='jsmin', output='scripts/app.js')

vendor_css = Bundle('vendor/bootstrap.min.css',
                    'vendor/bootstrap-multiselect.css',
                    output='styles/vendor.css')

vendor_js = Bundle(
    'vendor/jquery.min.js',
    'vendor/popper.min.js',
    'vendor/bootstrap.js',
    'vendor/bootstrap-multiselect.js',
    'vendor/tablesort.min.js',
    'vendor/zxcvbn.js',
    filters='jsmin',
    output='scripts/vendor.js')
