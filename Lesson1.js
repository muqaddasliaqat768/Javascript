// Hello World
console.log("Hello World");  //Run JS File in terminal use this command -> node Lesson1.js

//Variable (hold certain information)
var firstName="Muqaddas";
let lastName="Liaqat";
console.log(firstName);

//constants
const occupation="Software Engineer";
console.log(occupation);

//data types
var middleName="Ali"; //string
var ageOfBrother=25; //number
var isSheMarried=false; //boolean
var yearInMarried=null; //No value (null used)
var numberOfCars=undefined //error state (undefine)

//Concatenation & Interpolation
var price=50;
var itemName="Cup";
var messageToPrint="The price of your " + itemName+ " is " +price+ " dollars"; //concatenation
var messageToPrint2=`The price of your ${itemName} is ${price} dollars`; //interpolation (variable is define inside the string)
console.log(messageToPrint);
console.log(messageToPrint2);

//Objects (hold multiple information at the same time in key & value pair)
var customer={
    firstName:'Muqaddas',
    lastName:'Liaqat',
    age:30,
    cars: ["Toyota","Honda","Ford"] //add array in object
}
console.log(customer);
console.log(customer.firstName); //accessing object specific value  using dot notation
console.log(customer['firstName']); //accessing object specific value  using bracket notation   
console.log(`${customer.firstName} ${customer.lastName}`); //interpolation with object properties


//Arrays (list of items)
var car=["Toyota","Honda","Ford"];
car[1]="BMW"; //Replace value
console.log(car[1])
console.log(customer.cars[0]);


//Relational or comparison operators

//// > - More than
//// < - Less than
//// >= - More than equal
//// <= - Less than equal

var result = 10 > 5;
console.log(result); 


//Equality Operators
var x=1;
console.log(x == '1'); //loose comparison (only check the value)
console.log(x === '1'); //strict comparison (check value and datatype both)

//Logical 'AND'
console.log(true && true); //both values should be true

//Logical 'OR'
console.log(true || false); //one of the values should be true

//Logical 'NOT'
console.log(!true); //negation (inverts the boolean value)
console.log(6 !== 10);

//Conditional Statement 
//Question: 
  // if hour between 6 to 12 print "Good Morning"
  // if hour between 12 to 18 print "Good Afternoon"
  // otherwise print "Good Evening"

  var hour=5;
  if(hour >=6 && hour<=12){
    console.log("Good Morning");
}
else if (hour >=12 && hour<=18){
    console.log("Good Afternoon");
}
else{
    console.log("Good Evening");
}

//Loops (Repeat same word multiple times then we use loop)
//1. for loop (for i loop)
for(let i=0; i<5; i++){
    console.log("Hello World! " + i); //i is a counter variable
}

//2. for of loop
var cars=["Toyota","Honda","Ford"];
for(let car of cars){
    console.log(car); //car is a variable that holds each value of the array    
    if(car =="Honda"){
        break;
    }
}


//Functions (Organize code into reusable blocks , if we want to use the same code again and again we just copy the functionality and use it in another place where we want)
//1. Declarative Function (This function have a name and if we call the function before declaration, it will still work)

function helloOne(){ //declare function
    console.log("Hello 1");
}
helloOne(); //calling function


//2. Anonymous Function (This function does not have a name and and if we call the function before declaration, it will not work, throw an error)
var helloTwo=function(){ //declare function
    console.log("Hello 2");
}

helloTwo(); //calling function

//3. Function with single argument
function printName(name){
    console.log(name)
}

printName("Mike"); //calling function with argument

//4. Function with Multiple arguments
function printFullName(firstname, lastName){
    console.log(firstname + " " + lastName);
}
printFullName("Mike", "Smith"); //calling function with multiple arguments


//Function with return
function multipleByTwo(number){
    var result = number * 2;
    return result;
}

var myResult=multipleByTwo(5);
console.log(myResult); //calling function with return value

// //import function
// import {printAge} from "../Javascript Fundamentals/helpers/printHelpers"; //importing function from another file
// printAge(30); //calling imported function


//class & method
 class Person{

    printFirstName(firstName){                              // Method
        console.log("Your Name is" + " " + firstName);
    }
 }

var person = new Person(); //create instance of class
person.printFirstName("John"); //calling method of class

