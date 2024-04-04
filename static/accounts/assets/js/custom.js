// Function to toggle visibility of different search options
function toggleSearchOption(option) {
  document.getElementById("findDirections").style.display = option === 'findDirections' ? "block" : "none";
  document.getElementById("nearbyStations").style.display = option === 'nearbyStations' ? "block" : "none";
  document.getElementById("specificBus").style.display = option === 'specificBus' ? "block" : "none";
}

// Function to get user's geolocation
function getUserLocation() {
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
          var lat = position.coords.latitude;
          var lng = position.coords.longitude;
          var latLng = lat + "," + lng;
          console.log(latLng);
          document.getElementById("userLocation").value = latLng;
          document.getElementById("passLat").click();
      });
  } else {
      console.log("Geolocation is not supported by this browser.");
  }
}

// Function to reset axis images
function resetAxisImages() {
  var axisImages = document.getElementById('axis').getElementsByTagName('img');
  axisImages[0].classList.remove('move-right');
  axisImages[1].classList.remove('move-left');
}

// Initialize axis images on window load
window.addEventListener('load', resetAxisImages, false);

// Function for table searching
$(document).ready(function() {
  $("#myInput").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#myTable tr").filter(function() {
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
      });
  });
});

// Function for autocomplete search
function autocomplete(input, arr) {
  var currentFocus;
  input.addEventListener("input", function() {
      var val = this.value;
      closeAllLists();
      if (!val) { return false; }
      currentFocus = -1;
      var div = document.createElement("DIV");
      div.setAttribute("id", this.id + "autocomplete-list");
      div.setAttribute("class", "autocomplete-items");
      this.parentNode.appendChild(div);
      for (var i = 0; i < arr.length; i++) {
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
              var suggestion = document.createElement("DIV");
              suggestion.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
              suggestion.innerHTML += arr[i].substr(val.length);
              suggestion.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
              suggestion.addEventListener("click", function() {
                  input.value = this.getElementsByTagName("input")[0].value;
                  closeAllLists();
              });
              div.appendChild(suggestion);
          }
      }
  });
  input.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
          currentFocus++;
          addActive(x);
      } else if (e.keyCode == 38) {
          currentFocus--;
          addActive(x);
      } else if (e.keyCode == 13) {
          e.preventDefault();
          if (currentFocus > -1) {
              if (x) x[currentFocus].click();
          }
      }
  });
  function addActive(x) {
      if (!x) return false;
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
      for (var i = 0; i < x.length; i++) {
          x[i].classList.remove("autocomplete-active");
      }
  }
  function closeAllLists(elmnt) {
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
          if (elmnt != x[i] && elmnt != input) {
              x[i].parentNode.removeChild(x[i]);
          }
      }
  }
  document.addEventListener("click", function(e) {
      closeAllLists(e.target);
  });
}

var places = ["Kencom", "Afya center", "odeon", "OTC", "Koja", "Archives", "Railways", "Muthurwa", "Country Bus", "Ngara", "Ambassador", "Nyamakima", "Imenti House", "GPO"];
var busName = ["Supermetro", "Lopha Travellers", "MSL", "Metrotrans", "Nangkis", "Starbus", "Nicco", "citihopa", "KBS", "NTVRS", "Enabled", "Expresso", "Ngumoline", "Eightways", "KMOS", "Aldana", "Killeton", "Embassava", "Double M", "Ummoiner", "R.O.G", "Obamana", "Rembo Shuttle", "Orokise", "Latema", "2NK", "Zamzam", "KMO", "Tawala Sacco", "", "Mataara Sacco", "Lothian", "", "Agro House", "Lopha", "Eastleigh", "KMOS"];

document.addEventListener("DOMContentLoaded", function() {
  autocomplete(document.getElementById("myInput"), busName);
  autocomplete(document.getElementById("inputFrom"), places);
  autocomplete(document.getElementById("inputTo"), places);
});






















































// // ...................SEARCHBAR CHANGING........................ 
// function findDerections() {
//   document.getElementById("findDerections").style.display = "block";
//   document.getElementById("nearbyStations").style.display = "none";
//   document.getElementById("specificBus").style.display = "none";
// }

// function nearbyStations() {
//   document.getElementById("findDerections").style.display = "none";
//   document.getElementById("nearbyStations").style.display = "block";
//   document.getElementById("specificBus").style.display = "none";
// }

// function specificBus() {
//   document.getElementById("findDerections").style.display = "none";
//   document.getElementById("nearbyStations").style.display = "none";
//   document.getElementById("specificBus").style.display = "block";
// }
// // ...................SEARCHBAR CHANGING........................ 


// // ..............GOOGLE MAP.................. 
// // get and passing location 
// var lat = "";

// function getLocation() {
// if (navigator.geolocation) {
//   navigator.geolocation.getCurrentPosition(showPosition);
    
// } else {
//   lat = "Geolocation is not supported by this browser.";
//   console.log(lat);
// }
// }

// function showPosition(position) {
// lat = position.coords.latitude + "," + position.coords.longitude;
// console.log(lat);
// document.getElementById("userLocation").value = lat;
// document.getElementById("passLat").click();
// }
// // ..............GOOGLE MAP.................. 

// // ..............MOVING BUS.................. 
// function initialiseAxisImages() {
// var axis = document.getElementById('axis');
// var axisImages = axis.getElementsByTagName('img');

// axisImages[0].classList.remove('move-right');
// axisImages[1].classList.remove('move-left');
// }

// window.addEventListener('load', initialiseAxisImages, false);
// // ..............MOVING BUS.................. 

// // ..............TABLE SEARCHING.................. 
// $(document).ready(function(){
// $("#myInput").on("keyup", function() {
//   var value = $(this).val().toLowerCase();
//   $("#myTable tr").filter(function() {
//     $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
//   });
// });
// });
// // ..............TABLE SEARCHING.................. 



// // ....................................SEARCH SUGGESTION ....................................... 
// function autocomplete(inp, arr) {

// var currentFocus;

// inp.addEventListener("input", function(e) {
//     var a, b, i, val = this.value;
  
//     closeAllLists();
//     if (!val) { return false;}
//     currentFocus = -1;
  
//     a = document.createElement("DIV");
//     a.setAttribute("id", this.id + "autocomplete-list");
//     a.setAttribute("class", "autocomplete-items");
 
//     this.parentNode.appendChild(a);
//     for (i = 0; i < arr.length; i++) {
//       if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
//         b = document.createElement("DIV");
//         b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
//         b.innerHTML += arr[i].substr(val.length);
//         b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
//         b.addEventListener("click", function(e) {
//             inp.value = this.getElementsByTagName("input")[0].value;
//             closeAllLists();
//         });
//         a.appendChild(b);
//       }
//     }
// });
// inp.addEventListener("keydown", function(e) {
//     var x = document.getElementById(this.id + "autocomplete-list");
//     if (x) x = x.getElementsByTagName("div");
//     if (e.keyCode == 40) {
    
//       currentFocus++;
//       addActive(x);
//     } else if (e.keyCode == 38) { 
//       currentFocus--;
//       addActive(x);
//     } else if (e.keyCode == 13) {
//       e.preventDefault();
//       if (currentFocus > -1) {
//         if (x) x[currentFocus].click();
//       }
//     }
// });
// function addActive(x) {
//   if (!x) return false;
//   removeActive(x);
//   if (currentFocus >= x.length) currentFocus = 0;
//   if (currentFocus < 0) currentFocus = (x.length - 1);
//   x[currentFocus].classList.add("autocomplete-active");
// }
// function removeActive(x) {
//   for (var i = 0; i < x.length; i++) {
//     x[i].classList.remove("autocomplete-active");
//   }
// }
// function closeAllLists(elmnt) {
//   var x = document.getElementsByClassName("autocomplete-items");
//   for (var i = 0; i < x.length; i++) {
//     if (elmnt != x[i] && elmnt != inp) {
//       x[i].parentNode.removeChild(x[i]);
//     }
//   }
// }
// document.addEventListener("click", function (e) {
//     closeAllLists(e.target);
// });
// }

// var places = ["Kencom", "Afya center", "odeon", "OTC", "Koja", "Archives", "Railways", "Muthurwa", "Country Bus", "Ngara", "Ambassador", "Nyamakima", "Imenti House", "GPO",];
// var busName = ["Supermetro", "Lopha Travellers", "MSL", "Metrotrans", "Nangkis", "Starbus", "Nicco", "citihopa", "KBS", "NTVRS", "Enabled", "Expresso", "Ngumoline", "Eightways", "KMOS", "Aldana", "Killeton", "Embassava", "Double M", "Ummoiner", "R.O.G", "Obamana", "Rembo Shuttle", "Orokise", "Latema", "2NK", "Zamzam", "KMO", "Tawala Sacco", "", "Mataara Sacco", "Lothian", "", "Agro House", "Lopha", "Eastleigh", "KMOS",];

// document.addEventListener("DOMContentLoaded", function() {
//   autocomplete(document.getElementById("myInput"), busName);
//   autocomplete(document.getElementById("inputFrom"), places);
//   autocomplete(document.getElementById("inputTo"), places);
// });

// // .............................................SEARCH SUGGESTION.................................................... 
