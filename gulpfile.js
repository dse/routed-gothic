import gulp from "gulp";
import gulpSass from "gulp-sass";
import sassPkg from "sass";
import browserSync from "browser-sync";

const sass = gulpSass(sassPkg);

const srcStyles = "src/styles";
const destStyles = "public/fonts/routed-gothic/css";

const sassConfig = {
    quietDeps: true,
};

function sassTask() {
    return gulp.src(`${srcStyles}/app.scss`)
               .pipe(sass(sassConfig))
               .pipe(gulp.dest(`${destStyles}`));
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

export { sassTask as sass };
export { serveTask as serve };
