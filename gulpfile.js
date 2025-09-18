var gulp          = require('gulp');
var browserSync   = require('browser-sync').create();
var $             = require('gulp-load-plugins')();
var autoprefixer  = require('autoprefixer');

var sassPaths = [
    'node_modules/foundation-sites/scss',
    'node_modules/motion-ui/src'
];

function sassDev() {
    return sass({ dev: true });
}
function sassProd() {
    return sass();
}
function sass(options) {
    var dev = options && options.dev;
    var sassOptions = {
        includePaths: sassPaths
    };
    var renamePipe;
    if (dev) {
        renamePipe = $.util.noop();
    } else {
        sassOptions.outputStyle = 'compressed';
        renamePipe = $.rename({
            suffix: '.min'
        });
    }
    return gulp.src('src/scss/app.scss')
        .pipe($.sass(sassOptions).on('error', $.sass.logError))
        .pipe($.postcss([
            autoprefixer({ browsers: ['last 2 versions', 'ie >= 9'] })
        ]))
        .pipe(renamePipe)
        .pipe(gulp.dest('public/css'))
        .pipe(browserSync.stream());
}

function serve() {
    browserSync.init({
        server: "./public/"
    });
    gulp.watch("src/scss//*.scss", sass);
    gulp.watch("./public//*.html").on('change', browserSync.reload);
}

gulp.task('sassDev', sassDev);
gulp.task('sassProd', sassProd);
gulp.task('sass', gulp.series('sassDev', 'sassProd'));
gulp.task('serve', gulp.series('sass', serve));
gulp.task('default', gulp.series('sass', serve));
