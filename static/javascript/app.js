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
	console.log(response.data.message);
	const modalHTML = generateModalHTML(response.data);
	$('body > .container').append(modalHTML);
	$('#myModal').modal('show');
}

function generateModalHTML(data) {
	return `<div id="myModal" class="modal" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">${data.message}</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p>${data.message}</p>
      </div>
      <div class="modal-footer">
        <a class="btn btn-primary text-white" href="/groceries") }}">Go to Shopping List</a>
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>`;
}
