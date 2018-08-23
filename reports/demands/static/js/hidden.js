function RevealInput() {
    switch ($('#approve_rejection').val()) {
        case 'Approve':
            $("#hiddenInputContainer ").hide();
            break;

        case 'Reject':
            $("#hiddenInputContainer ").show();
            break;

        case '--------':
            $("#hiddenInputContainer ").hide();
            break;
    }
}

// $(function() {
//     $('#approve_rejection').change(function() {
//         RevealInput();
//     });

//     RevealInput();
// });