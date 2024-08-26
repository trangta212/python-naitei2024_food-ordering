console.log("working fine!")

$("#commentForm").submit(function(e){
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        
        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",
        
        success: function(response){            
            if (response.bool) {
                $("#review-res").html("Review added successfully!");
                $(".hide-comment-form").hide();
                $(".add-review").hide();

                var starsHtml = '';
                for (let i = 1; i <= 5; i++) {
                    if (i <= response.context.rating) {
                        starsHtml += '<i class="fas fa-star text-warning"></i>'; // Filled star
                    } else {
                        starsHtml += '<i class="far fa-star text-muted"></i>'; // Empty star
                    }
                }

                var newReviewHtml = `
                    <li class="reviews-members pt-4 pb-4">
                        <div class="media">
                            <a href="#" class="avatar-link">
                                <img 
                                    alt="Reviewer Avatar" 
                                    src="https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp" 
                                    class="reviewer-avatar"
                                >
                            </a>
                            <div class="media-body">
                                <div class="reviews-members-header">
                                    <div class="user-info">
                                        <h6 class="mb-1"><a class="text-black" href="#">${response.context.user}</a></h6>
                                        <!-- <p class="text-gray">Tue, 20 Mar 2020</p> -->
                                    </div>
                                </div>
                                <div class="reviews-members-body">
                                    <p class="rating-display">
                                        ${starsHtml}
                                    </p>
                                    <p>${response.context.comment}</p>
                                </div>
                            </div>
                        </div>
                    </li>
                `
                $(".existing-reviews").append(newReviewHtml);
            }
        }
    })
})
