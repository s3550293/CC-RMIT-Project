var matches = 0;
var user = document.getElementById("User");
var matchOne = document.getElementById("MatchOne");
var matchTwo = document.getElementById("MatchTwo");
var matchThree = document.getElementById("MatchThree");

function matchFound(){
    matches++;
    if(matches == 1){
        user.style.width = "50%";
        matchOne.style.width = "50%";
        matchOne.style.left = "50%";
    }
    if(matches == 2){
        user.style.width = "33.33%";
        matchOne.style.width = "33.33%";
        matchTwo.style.width = "33.33%";
        matchOne.style.left = '33.33%';
        matchTwo.style.left = '66.66%';
    }
    if(matches == 3){
        user.style.width = "25%";
        matchOne.style.width = "25%";
        matchTwo.style.width = "25%";
        matchThree.style.width = "25%";
        matchOne.style.left = '25%';
        matchTwo.style.left = '50%';
        matchThree.style.left = '75%';
    }
}

function cancelMatch() {
    matches--;
    if(matches == 1){
        user.style.width = "50%";
        matchOne.style.width = "50%";
        matchOne.style.left = "50%";
    }
    if(matches == 2){
        user.style.width = "33.33%";
        matchOne.style.width = "33.33%";
        matchTwo.style.width = "33.33%";
        matchOne.style.left = '33.33%';
        matchTwo.style.left = '66.66%';
    }
}

function resetMatches(){
    matches = 0;
    user.style.width = "100%";
    matchOne.style.width = "100%";
    matchTwo.style.width = "50%";
    matchThree.style.width = "33.33%";
    matchOne.style.left = 0;
    matchTwo.style.left = 0;
    matchThree.style.left = 0;
}

$(function(){
  
    $(".dropdown-game-menu a").click(function(){
      
      $(".btnGame:first-child").text($(this).text());
       $(".btnGame:first-child").val($(this).text());
    });
  
  });