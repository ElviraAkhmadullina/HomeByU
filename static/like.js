"use strict";

$('document').ready(function() {
    function changeButton(results) {
        if (results.confirm === true) {
            let theLikeButton = $('#' + String(results.id));
            theLikeButton.attr('style', "color:red");
        }
    }
    
    function likePost(evt) {
        $.post('/like', {'postId': this.id}, changeButton);
    }

    
    $('.like').on('click', likeArticle);
    
});
