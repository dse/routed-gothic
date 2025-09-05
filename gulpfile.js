/*global console */

import fs            from 'node:fs';
import { Transform } from 'node:stream';

import autoprefixer  from 'autoprefixer';
import browsersync   from 'browser-sync';
import { globSync }  from 'glob';
import gulp          from 'gulp';
import data          from 'gulp-data';
import nunjucks      from 'gulp-nunjucks-render';
import postcss       from 'gulp-postcss';
import gulpSass      from 'gulp-sass';
import nodeSass      from 'node-sass';
import * as rollup   from 'rollup';
import babel         from '@rollup/plugin-babel';
import resolve       from '@rollup/plugin-node-resolve';

console.log(nodeSass);

const sass = gulpSass(nodeSass);

let server;

const excludePartials = ['!**/_*', '!**/_*/**/*'];

const sassPaths = [
    '.',
    // '../../node_modules/foundation-sites/scss',
    // '../../node_modules/motion-ui/src'
];
const sassOptions = {
    includePaths: sassPaths,
};
const nunjucksOptions = {
    path: 'src/pages',
};

function sassTask() {
    console.log(`sassTask: executing`);
    return gulp.src(['src/styles/**/*.scss', ...excludePartials])
               .pipe(compilingMessageGenerator())
               .pipe(sass(sassOptions))
               .pipe(postcss([autoprefixer]))
               .pipe(gulp.dest('dist/styles'))
               .pipe(wroteMessageGenerator());
}

function plainHtmlTask() {
    return gulp.src(['src/pages/**/*.html', ...excludePartials])
               .pipe(compilingMessageGenerator())
               .pipe(gulp.dest('dist/web'))
               .pipe(wroteMessageGenerator());
}

let siteData;
function buildSiteData() {
    if (siteData) {
        return siteData;
    }
    siteData = {};
    for (const filename of globSync('src/data/**/*.json')) {
        Object.assign(siteData, JSON.parse(fs.readFileSync(filename, 'utf-8')));
    }
    return siteData;
}

function nunjucksHtmlTask() {
    return gulp.src(['src/pages/**/*.njk', ...excludePartials])
               .pipe(data(function (file) {
                   return JSON.parse(JSON.stringify(buildSiteData()));
               }))
               .pipe(compilingMessageGenerator())
               .pipe(nunjucks(nunjucksOptions))
               .pipe(gulp.dest('dist/web'))
               .pipe(wroteMessageGenerator());
}

function compilingMessageGenerator() {
    return new Transform({
        objectMode: true,
        transform(record, encoding, callback) {
            console.log(`compiling ${record.path}`);
            this.push(record);
            callback(null);
        }
    });
}

function wroteMessageGenerator() {
    return new Transform({
        objectMode: true,
        transform(record, encoding, callback) {
            console.log(`wrote ${record.path}`);
            this.push(record);
            callback(null);
        }
    });
}

const htmlTask = gulp.parallel(plainHtmlTask, nunjucksHtmlTask);

function rollupTask() {
    console.log(`rollupTask: executing`);
    return rollup
        .rollup({ input: 'src/scripts/clock-page.js',
                  plugins: [resolve(), babel({ babelHelpers: 'bundled' })] })
        .then(bundle => {
            console.log(`rollupTask: generating bundle`);
            return bundle.write({
                file: './dist/scripts/app.js',
                format: 'umd',
                name: 'library',
            });
        });
}

function serverTask() {
    // never completes
    if (server) {
        return;
    }
    console.log(`serverTask: starting server`);
    server = browsersync.create();
    server.init({
        server: './dist',
    });
}

function reloadTask(cb) {
    console.log(`reloadTask: reloading server`);
    if (server) {
        server.reload();
    }
    cb();
}

function watchTask() {
    // never completes
    console.log(`watchTask: watching files`);
    gulp.watch('src/pages/**/*.html', gulp.series(htmlTask, reloadTask));
    gulp.watch('src/styles/**/*.scss', gulp.series(sassTask, reloadTask));
    gulp.watch('src/scripts/**/*.js', gulp.series(rollupTask, reloadTask));
}

const buildTask = gulp.parallel(sassTask, htmlTask, rollupTask);

const devTask = gulp.series(
    gulp.parallel(sassTask, htmlTask, rollupTask),
    gulp.parallel(serverTask, watchTask),
);

export { rollupTask as rollup };
export { sassTask   as sass   };
export { htmlTask   as html   };
export { buildTask  as build  };
export { devTask    as dev    };
