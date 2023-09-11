// $(document).ready(function() {
//     $('.toggle-follow').click(function() {
//         let $this = $(this);
//         let username = $this.data('username');
//         let action = $this.text().toLowerCase() === 'unfollow' ? 'follow' : 'unfollow';
//
//         $.ajax({
//             url: '/path/to/toggle/follow/', // change this to your actual URL
//             method: 'POST',
//             data: {
//                 'username': username,
//                 'action': action
//             },
//             success: function(response) {
//                 if (response.status === 'success') {
//                     if (action === 'follow') {
//                         $this.text('Follower');
//                     } else {
//                         $this.text('Unfollow');
//                     }
//                 }
//             }
//         });
//     });
// });
