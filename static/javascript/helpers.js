/*****************/
/*	  HELPERS	 */
/*****************/

function addSetinel() {
	$(createSentinelDivHTML()).insertAfter('#recipe-container');
	intersectionObserver.observe(document.querySelector('#sentinel'));
}

function displayResults(response) {
	$('main').children().slideUp('slow', function() {
		$(this).remove();
	});

	setTimeout(() => {
		const $h1 = makeH1();
		const $hr = makeHr();
		const $total = makeTotalResults(response.data.data);
		const $row = makeRow();
		$('main').prepend($h1).hide().slideDown('slow');
		$('h1').after($row).after($hr).after($total);
		response.data.data.results.forEach((recipe) => {
			showRecipeCard(recipe, response.data.data, response.data.favorites);
		});
		$('form').on('click', '.fa-heart', handleFavorite);
	}, 800);
}

function showRecipeCard(recipe, data, favorites) {
	const recipeHTML = generateRecipeCardHTML(recipe, data, favorites);
	$('#recipe-container').append(recipeHTML);
	$('form').on('submit', (e) => {
		e.preventDefault();
	});
}

function updateListContainer() {
	$('#list-container')
		.empty()
		.html(
			`<p class="text-center lead">Your list is empty!</p> <br> <a class="btn btn-outline-primary" href="/favorites">View Favorites</a>`
		);
}

function generateRecipeCardHTML(recipe, data, favorites) {
	let favButton;

	if (favorites.includes(recipe.id)) {
		favButton = `<button id="${recipe.id}" data-id="${recipe.id}" class='btn btn-sm'><span><i  class="fas fa-heart"></i></span></button>`;
	} else {
		favButton = `<button id="${recipe.id}" data-id="${recipe.id}" class='btn btn-sm'><span><i class="far fa-heart"></i></span></button>`;
	}

	return `<div class="card border mb-4 mx-auto p-2 rounded text-center">
	<a href="/recipes/${recipe.id}" class="card-link">
	<img src="${data.baseUri}${recipe.image}" class="card-img-top img-fluid" alt="Photo of ${recipe.title}">
	<div class="card-body py-2">
	  <h5 class="card-title d-inline">${recipe.title}</h5>
	  <form id="favorite-form" class="favorite-form d-inline">
		${favButton}
	  </form>
	  <p class="lead mb-0">Ready In: ${recipe.readyInMinutes} minutes</p>
	  <p class="lead">Servings: ${recipe.servings}</p>
	  <a class="small text-muted" href="${recipe.sourceUrl}">View original</a>
	  <br>
	  </a>
	</div>
</div>`;
}

function makeTotalResults(data) {
	let $newTotal = $('<p>').text(`${data.totalResults} total results`).addClass('small text-center text-dark');
	return $newTotal;
}

function makeH1(text = 'Easy Meals') {
	let $newH1 = $('<h1>').text(text).addClass('display-2 text-center');
	return $newH1;
}

function makeHr() {
	let $newHr = $('<hr>');
	return $newHr;
}

function makeRow() {
	let $newRow = $('<div>').addClass('row p-0 m-0').attr('id', 'recipe-container');
	return $newRow;
}

function showUpdateForm() {
	const id = $(this).data('id');
	const modalHTML = generateUpdateModalHTML(id);
	addShowModal(modalHTML);
	$('#submit-update').on('click', handleUserUpdate);
}

function updateProfile(response) {
	$('#user-email').text(`${response.data.user.email}`);
	$('#user-image').attr('src', `${response.data.user.img_url}`);
	$('.avatar').attr('src', `${response.data.user.img_url}`);
}

function toggleFavorite(response) {
	if (response.status !== 200) {
		displayErrorAlert(response);
	} else {
		$(this).toggleClass('fas fa-heart');
		$(this).toggleClass('far fa-heart');
		displaySuccessAlert(response);
	}
}

function displayErrorAlert(response) {
	console.log(`Error details: ${response.data.errors}`);
	$('.feedback').remove();
	const alertHTML = generateAlertHTML('Something went wrong, please try again', 'danger');
	$('main').prepend(alertHTML).alert();
	$('.feedback').hide().fadeIn('slow').delay(1000).fadeOut('slow');
}

function displaySuccessAlert(response) {
	$('.feedback').remove();
	const alertHTML = generateAlertHTML(response.data.message, 'success');
	$('main').prepend(alertHTML).alert();
	$('.feedback').hide().fadeIn('slow').delay(1000).fadeOut('slow');
}

function displaySuccessModal(response) {
	const modalHTML = generateRecipeModalHTML(response.data);
	if ($('#myModal')) {
		$('#myModal').remove();
	}
	addShowModal(modalHTML);
}

function displayAndRemove(data) {
	const $toRemove = $(this).closest('li');
	$toRemove.html(`${data.message}`);
	$toRemove.delay(500).fadeOut(2000);
}

function confirmRemove() {
	$(this).removeClass('far fa-trash-alt');
	$(this).addClass('fas fa-minus-circle');
	$(this)
		.attr('id', 'confirm-remove')
		.attr('data-toggle', 'tooltip')
		.attr('data-placement', 'right')
		.attr('title', 'Remove from list')
		.tooltip()
		.on('click', removeIngredientFromGroceryList)
		.tooltip('hide');
}

function showAddIngredient() {
	if ($('.add-ingredient').length !== 0) {
		return;
	}

	const newAddIngredient = makeAddIngredient();
	$(this).closest('li').before(newAddIngredient);
	$('.add-ingredient').on('submit', handleAddIngredient);
}

function makeAddIngredient() {
	return `<li class='list-group-item my-0 text-center'>
	<form class="add-ingredient form-inline d-inline">
	<input class="form-control" id="user-add-ingredient" type="text" placeholder="Add new ingredient..." required>
	<button type="submit" id="show-add-ingredient" class='btn btn-sm btn-outline-primary'>
	Add
	</button>
	</form>
	</li>
	`;
}

function generateIngredientHTML(ingredient) {
	return `
	${ingredient}
	<span class="btn" data-ingredient="${ingredient}">
	<i class="far fa-trash-alt remove"></i>
	</span>`;
}

function generateGroceryModalHTML(data) {
	return `<div id="myModal" class="modal" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
	<div class="modal-content">
	  <div class="modal-header">
		<p class="mx-auto my-0">${data.message}</p>
      </div>
	  <div class="modal-footer">
        <a class="btn btn-primary text-white ml-auto" href="/groceries") }}">Go to Shopping List</a>
        <button type="button" class="btn btn-secondary mr-auto" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>`;
}

function generateRecipeModalHTML(data) {
	return `<div id="myModal" class="modal" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document">
	<div class="modal-content">
	  <div class="modal-header">
		<p class="mx-auto my-0">${data.message}</p>
      </div>
	  <div class="modal-footer">
        <a class="btn btn-primary text-white ml-auto" href="/recipes/${data.recipe.id}") }}">Recipe Details</a>
        <button type="button" class="btn btn-secondary mr-auto" data-dismiss="modal">Thanks</button>
      </div>
    </div>
  </div>
</div>`;
}

function generateAlertHTML(message, category) {
	return `<div class="container w-25 mx-auto feedback">
	<div class="alert alert-${category} alert-dismissible fade show text-center" role="alert">
	${message}
	<button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
  </div>
  </div>`;
}

function addShowModal(modalHTML) {
	$('main').append(modalHTML);
	$('#myModal').modal('show');
}

function doNothingOnSubmit(evt) {
	evt.preventDefault();
	return;
}

function generateUpdateModalHTML(id) {
	return `<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModal" aria-hidden="true">
	<div class="modal-dialog" role="document">
	  <div class="modal-content">
		<div class="modal-header">
		  <h5 class="modal-title text-center">Update Profile</h5>
		  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
			<span aria-hidden="true">&times;</span>
		  </button>
		</div>
		<div class="modal-body">
		  <form id="user-update">
			<div class="form-group">
			  <label for="email" class="col-form-label">Email:</label>
			  <input type="text" class="form-control" id="email">
			</div>
			<div class="form-group">
			  <label for="img-url" class="col-form-label">Image URL:</label>
			  <input type="url" class="form-control" id="img-url">
			</div>
		  </form>
		</div>
		<div class="modal-footer">
		  <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
		  <button data-id="${id}" data-dismiss="modal" id="submit-update" type="button" class="btn btn-primary">Update</button>
		</div>
	  </div>
	</div>
  </div>`;
}

function createSentinelDivHTML() {
	return `<div class="d-flex justify-content-center mb-3" id="sentinel">
      <div class="spinner-border" role="status"></div>
    </div>`;
}
