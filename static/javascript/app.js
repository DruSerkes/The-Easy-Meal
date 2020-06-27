/* 
// ANIMATIONS
*/

// Flashed messages fade in, fade out
$(document).ready(function() {
	$('#flash').hide().delay(300).fadeIn(500).delay(3000).fadeOut(800);
});

/* 
// AJAX
*/

//
$('#add-ingredients').on('click', addIngredientsToGroceryList);

async function addIngredientsToGroceryList(evt) {
	const id = $(this).data('id');
	response = await axios.post(`/groceries`, (data = { id }));
	// Display response on DOM
}
