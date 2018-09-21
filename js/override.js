var matches = 0;
var user = document.getElementById("User");
var matchOne = document.getElementById("MatchOne");
var matchTwo = document.getElementById("MatchTwo");
var matchThree = document.getElementById("MatchThree");

function matchFound(){
    matches++;
    if(matches == 1){
        // user.classList.add('splitTwo');
        // matchOne.classList.add('splitTwo');
        user.style.width = "50%";
        matchOne.style.width = "50%";
        matchOne.style.right = 0;
    }
    if(matches == 2){
        // user.classList.remove('splitTwo');
        // matchOne.classList.remove('splitTwo');
        // user.classList.add('splitThree');
        // matchOne.classList.add('splitThree');
        // matchTwo.classList.add('splitThree');
        user.style.width = "33.33%";
        matchOne.style.width = "33.33%";
        matchTwo.style.width = "33.33%";
        matchOne.style.right = '33.33%';
        matchTwo.style.right = 0;
    }
    if(matches == 3){
        // user.classList.remove('splitThree');
        // matchOne.classList.remove('splitThree');
        // matchTwo.classList.remove('splitThree');
        // user.classList.add('splitFour');
        // matchOne.classList.add('splitFour');
        // matchTwo.classList.add('splitFour');
        // matchThree.classList.add('splitFour');
        user.style.width = "25%";
        matchOne.style.width = "25%";
        matchTwo.style.width = "25%";
        matchThree.style.width = "25%";
        matchOne.style.right = '50%';
        matchTwo.style.right = '25%';
        matchThree.style.right = 0;
    }
}

function resetMatches(){
    matches = 0;
    user.style.width = "100%";
    matchOne.style.width = "100%";
    matchTwo.style.width = "50%";
    matchThree.style.width = "33.33%";
    matchOne.style.right = 0;
    matchTwo.style.right = 0;
    matchThree.style.right = 0;
    // user.classList.remove('splitFour');
    // matchOne.classList.remove('splitFour');
    // matchTwo.classList.remove('splitFour');
    // matchThree.classList.remove('splitFour');
    
}