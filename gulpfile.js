import gulp from "gulp";
import gulpSass from "gulp-sass";
import sassPkg from "sass";
import browserSync from "browser-sync";
import { nunjucksCompile as nunjucks } from "gulp-nunjucks";

const sass = gulpSass(sassPkg);

const srcStyles = "src/styles";
const destStyles = "public/fonts/routed-gothic/css";
const srcPages = "src/pages";
const destPages = "public/fonts/routed-gothic";

const excludePartials = [`!**/_*`, `!**/_*/**/*`];

function sassTask() {
    return gulp.src(`${srcStyles}/app.scss`)
               .pipe(sass({
                   quietDeps: true,
               }))
               .pipe(gulp.dest(destStyles));
}

function pagesTask() {
    return gulp.src([`${srcPages}/**/*.njk`, ...excludePartials])
               .pipe(nunjucks())
               .pipe(gulp.dest(destPages));
}

function serveTask() {
    const server = browserSync.create();
    server.init({
        startPath: "/fonts/routed-gothic/",
        server: {
            baseDir: "./public",
        }
    });
}

const build = gulp.parallel(pagesTask, sassTask);

export { sassTask as sass };
export { serveTask as serve };
export { pagesTask as pages };
export { build };
