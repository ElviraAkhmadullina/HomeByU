"use strict";

$('document').ready(function() {
    function unlikePost(results) {
        if (results.confirm === true){
            let theDiv = $('#div-' + String(result.id));
            theDiv.remove();
        }
    }

    function likePost(env) {
        $.post('/unlike', {postId: this.id}, unlikePost);
    }

    $('.like').on('click', likePost);
})