var gulp = require('gulp'),
    imagemin = require('gulp-imagemin');


// compress images
gulp.task('default', function() {

});

// compress images
gulp.task('image', function() {
    gulp.src('images/*')
        .pipe(imagemin())
        .pipe (gulp.dest('images/'));
});
