$(document).ready(function createMemberTables() {
    var actives = [
        {title:"Charter", members: [
            "Jacob Ash", 
            "Nicholas Bowman",
            "Jackson Chandler",
            "Nicholas Endsley",
            "Nicholas Eschbacher", 
            "Earle Lariosa", 
            "David Lindsay", 
            "Jason Lohe", 
            "Ryan Mathewson", 
            "William Meyer", 
            "Jacob Sanders", 
            "Jackson Smith", 
            "Matthew Taylor", 
            "Spencer Tompkins", 
            "Kyle White", 
            "Ethan Wilken", 
            "Garret Wilt"
        ]},
        {title:"Alpha", members: [
            "Zack Becker", 
            "Carson Bettendorf",
            "Steven Biros",
            "Alec Foutch",
            "Austin Lambert",
            "Austin Laramie",
            "Ian Naeger", 
            "Gabe Ort", 
            "Brett Pawlak", 
            "Alex Salinas", 
            "Brett Surls", 
            "Cameron Warder",
            "John Wolken"
        ]},
        {title:"Beta", members: [
            //"Andres Acosta", 
            "Samuel Farinella",
            "Joshua Gabel", 
            "Matthew Gerstenkorn",
            //"Jamison Gjerde",
            "Austin Kirby",
            "Jackson Marsch", 
            "Brett Norman", 
            "Richard Oman", 
            "Kael Rademan", 
            "Braxton Salcedo", 
            //"Alec Short", 
            "Preston Sikes",
            "Nicholas Taylor", 
            "Connor Weiss", 
            "Christopher Whetsel"
        ]},
        {title:"Gamma", members: [
            "Bradley Atkinson", 
            "Peter Brandsgaard", 
            "Parker DuMontier",
            "Landen Eagan",
            "Nicholas O'Gorman", 
            "Hareen Patel",
            "Ryan Schowalter",
            "Corey Wands"
        ]},
        {title:"Delta", members: [
            "James Congdon",
            "Jacob Eastman", 
            "Josh Eastman", 
            "Marcos Ehinger",
            "Aaron Henry",
            "Austin Kimes",
            "Flynn McNeely",
            "Benjamin Musick",
            "Elhadji Ndiaye",
            "Brian Robinson",
            "Jake Shulman",
            "Stephen Sowers III",
            "Alex Stone",
            "Benjamin Thornbury",
            "Jayce Tschirgi",
            "Michael Winklemann"
        ]},
        {title:"Epsilon", members: [
            "Jack Murphy",
            "Kasen Rademan", 
            "Tom Scully", 
            "Josh Westbrook"
        ]},
        {title:"Zeta", members: [
            "Steven Cole Perrin",
            "Dameron Taylor",
            "Hunter Tucker",
            "Chase White"
        ]},
        {title:"Eta", members: [
            "Ben Casey",
            "Adam Kurzejeski",
            "Ethan Schutzenhofer",
            "Zech Watkins"
        ]},
	{title:"Theta", members: [
	    "Christian Ackert",
	    "Andrew Cable",
	    "Alex Centorbi",
	    "Tyler Corley",
	    "Zachary Gasca",
	    "Alec Glascock",
	    "Calum Hathcock",
	    "Christian Kerbler",
	    "Jeffrey Kerley",
	    "Thomas Langdon",
	    "Juan Martinez",
	    "Karsten McMillan",
	    "Dalton Roberts",
	    "Jacob Salka",
	    "Chance Wilhite",
	    "Eric Wiseman",
	    "Sofonyas Woldekidan",
	    "Philip Wu",
	    "Sebastian Zheng",
	    "Christoph Zuehlke"
	]}
    ];
    
    var alumHeads = [
		"Alumni",
		"Class",
		"Graduated",
		"Current Employment"
		
	];
    
	var alumni = [
        {name:"Jacob Ash", date:"Spring 2018", work:"GKN Aerospace", class:"Charter"},
		{name:"Weston Basquette", date:"N/A", work:"N/A", class:"Beta"},
        {name:"Steven Biros", date:"Spring 2018", work:"US Coast Guard", class:"Alpha"},
		{name:"Christopher Blasius", date: "Spring 2015", work: "Johnson Health Tech North Amrc", class: "Charter"},
        {name:"Nicholas Bowman", date:"Spring 2018", work:"Antolin Nashville", class:"Charter"},
        {name:"Peter Brandsgaard", date:"Spring 2018", work:"HDR", class:"Gamma"},
		{name:"Daniel Brewer", date: "Fall 2016", work: "Mississippi Lime Company", class: "Charter"},
		{name:"Michael Brooks", date: "Fall 2016", work: "Boeing", class: "Charter"},
		{name:"Arvin Bustos", date: "Spring 2015", work: "University of Iowa", class: "Charter"},
        {name:"Jackson Chandler", date: "Fall 2017", work: "Hallmark Cards", class: "Charter"},
		{name:"Alexander Chung", date: "Fall 2016", work: "Honeywell", class: "Charter"},
		{name:"Kevan Clarke", date: "Fall 2016", work: "Synergy Mechanical Solutions, Inc.", class: "Charter"},
		{name:"James Clynes", date: "Spring 2016", work: "MoDOT", class: "Charter"},
		{name:"Justin Distler", date: "Spring 2016", work: "Black & Veatch", class: "Charter"},
        {name:"Nicholas Endsley", date:"Spring 2017", work:"AZZ / Central Electric", class:"Charter"},
        {name:"Nicholas Eschbacher", date: "Fall 2017", work: "Burns & McDonnell", class: "Charter"},
		{name:"Calvin Irwin", date: "Fall 2014", work: "US Peace Corps", class: "Charter"},
        {name:"Austin Lambert", date:"Spring 2018", work:"SpaceX", class:"Alpha"},
        {name:"Austin Laramie", date:"Spring 2017", work:"H-J Enterprises, Inc.", class:"Alpha"},
        {name:"David Lindsay", date:"Spring 2017", work:"CaptiveAire Systems", class:"Charter"},
        {name:"Jason Lohe", date: "Fall 2017", work: "DRS Technologies, Inc.", class: "Charter"},
        {name:"Ryan Mathewson", date:"Spring 2017", work:"NASA", class:"Charter"},
		{name:"Grahm Meyer", date: "Fall 2016", work: "AZZ / Central Electric", class: "Alpha"},
        {name:"William Meyer", date: "Fall 2017", work: "Timken Belts", class: "Charter"},
		{name:"Dominic Montoia", date: "Spring 2016", work: "ESD", class: "Alpha"},
        {name:"Elhadji Ndiaye", date:"Spring 2018", work:"", class:"Delta"},
        {name:"Brett Norman", date: "Fall 2017", work: "Stroco Manufacturing, Inc.", class: "Beta"},
        {name:"Brett Pawlak", date:"Spring 2018", work:"", class:"Charter"},
		{name:"Ethan Roussin", date: "Fall 2016", work: "TriMedx", class: "Charter"},
        {name:"Alex Salinas", date:"Spring 2017", work:"Life Spine, Inc.", class:"Alpha"},
        {name:"Jacob Sanders", date: "Fall 2017", work: "Black & Veatch", class: "Charter"},
        {name:"Ryan Schowalter", date:"Spring 2018", work:"", class:"Gamma"},
		{name:"Chase Skawinski", date: "Fall 2016", work: "CRB", class: "Charter"},
        {name:"Jackson Smith", date:"Spring 2018", work:"Schneider Electric", class:"Charter"},
		{name:"Paul Smith", date: "Spring 2015", work: "Gits Manufacturing", class: "Charter"},
        {name:"Brett Surls", date:"Spring 2017", work:"AZZ / Central Electric", class:"Alpha"},
        {name:"Matthew Taylor", date: "Fall 2017", work: "National Design Build Services", class: "Charter"},
        {name:"Spencer Tompkins", date: "Fall 2017", work: "Honeywell", class: "Charter"},
		{name:"Wenbin Wan", date: "Fall 2016", work: "N/A", class: "Alpha"},
		{name:"Jesse White", date: "Fall 2016", work: "HBK Engineering, LLC", class: "Charter"},
        {name:"Kyle White", date: "Fall 2017", work: "Dynamic Engineered Systems", class: "Charter"},
        {name:"Ethan Wilken", date:"Spring 2017", work:"GKN Aerospace", class:"Charter"},
        {name:"John Wolken", date:"Spring 2018", work:"HNTB Corporation", class:"Alpha"}
	];
	
    // set largestSize to charter class size
	var largestSize = actives[0].members.length;
	var tableS = '<table  class="table table-responsive"><thead><tr id="activesTableHead">'; 
	var tableH = "";
	var tableM = '</tr></thead><tbody id="activesTableBody">';
	var tableB = "";
	var tableE = '</tbody></table>';
	
	populateActivesTableHead();
	populateActivesTableBody();
//	console.log("tabelS: " + tableS);
//	console.log("tabelH: " + tableH);
//	console.log("tabelM: " + tableM);
//	console.log("tabelB: " + tableB);
//	console.log("tabelE: " + tableE);
	$("#membersTable").append(tableS + tableH + tableM + tableB + tableE);
	
	tableS = '<table  class="table table-responsive"><thead id="alumniTableHead"><tr>';
	tableM = '</tr></thead><tbody>';

	populateAlumniTableHead();
	populateAlumniTableBody();
	$("#alumniTable").append(tableS + tableH + tableM + tableB + tableE);
    
    // Use jQuery floatThead to maintain table headers while scrolling
    $table = $('.tableWrapper table');
    $table.floatThead({
        scrollContainer: function ($table) {
            return $table.closest('.tableWrapper');
        }
    });

	function populateActivesTableHead() {
		//$doc = $("#activesTableHead");
		/* $.each(classes, function(index, str) {
			//$doc.append("<th>" + str + "</th>")
			tableH += "<th>" + str + "</th>";
		}); */
        $.each(actives, function(index, obj) {
            tableH += "<th>" + obj.title + " Class</th>";
        });
	}
	function populateAlumniTableHead() {
		tableH = "";
		//$doc = $("#activesTableHead");
		$.each(alumHeads, function(index, str) {
			//$doc.append("<th>" + str + "</th>")
			tableH += "<th>" + str + "</th>";
		});
	}
	function populateActivesTableBody() {
		findLargest();
		
        for(i = 0; i < largestSize; i++) {
            tableB += "<tr>";
            $.each(actives, function(index, obj) {
                if(i < obj.members.length) {
                    tableB += "<td>" + obj.members[i] + "</td>";
                }else {
                    tableB += "<td></td>";
                }
            })
            tableB += "</tr>";
        }
	}
	
	function populateAlumniTableBody() {
		tableB = "";
		for(i=0; i<alumni.length; i++) {
			tableB += "<tr>";
			tableB += "<td>" + alumni[i].name + "</td>";
			tableB += "<td>" + alumni[i].class + "</td>";
			tableB += "<td>" + alumni[i].date + "</td>";
			tableB += "<td>" + alumni[i].work + "</td>";
			
			tableB += "</tr>";
		}
	}
	function findLargest() {
		$.each(actives, function(index, obj) {
            if(obj.members.length > largestSize) {
                largestSize = obj.members.length;
            }
        });	
	}
	
});
