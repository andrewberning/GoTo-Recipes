let recipesList = $("#recipes-list")
let favoritesList = $("#favorites-list")
let singleRecipe = $(".container")
let viewMoreBtn = $("#view-more-btn")

let pageNumber = 1

/** clear the list */
function clearRecipesList() {
  recipesList.empty();
  checkDivContent();
}


/** check if list has content and show "view-more" button */
function checkDivContent() {
  if ($.trim(recipesList.html()) === "") {
    viewMoreBtn.hide();
  } else {
    viewMoreBtn.show();
  }
}


/** given data about a recipe, generate html */
function generateRecipeHTML(recipe) {
  return `
    <div class="recipe-container col" data-id=${recipe.id}>
      <div class="recipe-card card h-100">
        <img class="recipe-img card-img-top"
            src="${recipe.image}"
            alt="${recipe.title}">
        <div class="card-body">  
          <h5 class="card-title">
            <a href="/getRecipe/${recipe.id}">${recipe.title}</a>
          </h5>
        </div>
        <button class="save-btn btn btn-success">Add to favorites</button>
      </div>
    </div>
  `;
}


/** get recipe function */
async function getRecipes(query, page) {
  const response = await axios.get(`/recipes/${query}/${page}`)
  
  for (let recipeData of response.data) {
    let recipe = $(generateRecipeHTML(recipeData));
    recipesList.append(recipe);
  }
  checkDivContent();
}

/** get random recipes */
async function getRandomRecipes() {
  const response = await axios.get("/random_recipes")

  for (let recipeData of response.data) {
    let recipe = $(generateRecipeHTML(recipeData));
    recipesList.append(recipe);
  }
}


/** handle form for searching recipes */

$("#search-form").on("submit", function(evt) {
  evt.preventDefault();
  // clear the current list
  clearRecipesList();
  
  // grab the value in the search input
  const query = $('#query').val();
  
  pageNumber = 1

  getRecipes(query, pageNumber);

});

/** handle random button click */

$("#random-btn").on("click", function() {
  $("#query").val("")
  clearRecipesList();
  checkDivContent();
  getRandomRecipes();
})

/** handle view more button */
$("#view-more-btn").on("click", function() {
  let query = $('#query').val();
  pageNumber+=1;

  getRecipes(query, pageNumber);
  
})


/** create an event delegation to listen for a click on the remove button to delete a recipe on the frontend and remove it from the database */
favoritesList.on("click", ".remove-btn", async function (evt) {
  evt.preventDefault();
  let recipeContainer = $(this).closest('.recipe-container');
  let recipeId = recipeContainer.data("id");

  await axios.delete(`/users/favorites/${recipeId}`);
  recipeContainer.remove();
  
})

singleRecipe.on("click", ".remove-btn", async function (evt) {
  evt.preventDefault();
  let recipeContainer = $(this).closest('.container');
  let recipeId = recipeContainer.data("id");

  await axios.delete(`/users/favorites/${recipeId}`)

})


/** create and event delegation to listen for a click on the add to favorites button to add recipe to favorites list to the database. */
recipesList.on("click", ".save-btn", async function (evt) {
  evt.preventDefault();
  const recipeBtn = $(this);
  const recipeContainer = $(this).closest('.recipe-container');

  const recipeId = recipeContainer.attr('data-id');
  const recipeTitle = recipeContainer.find('.card-title').text().trim();
  const recipeImage = recipeContainer.find('.recipe-img').attr('src');

  await axios.post(`/users/favorites/add`, {
    recipeId,
    recipeTitle,
    recipeImage
  });
});


