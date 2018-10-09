$(document).ready(function() {
	createFooter(); 
	
	function createFooter() {
	var str = '<div id ="footerWrapper"><div id="innerFooterWrapper"><div class="collumn1" ><img src="coat.png" height = 100px width=100px/></div><p id="collumn2">Contact For Organization: <br> <a style="text-decoration:none; color:white;" href="mailto:beta-omicron@sigmaphidelta.org">beta-omicron@sigmaphidelta.org</a> </p><p id="collumn2">Contact For Recruitment: <br> <a style="text-decoration:none; color:white;" href="mailto:recruitment@spdmizzou.org">recruitment@spdmizzou.org</a> </p><p id = "collumn2"> Contact For Webmaster: <br><a style="text-decoration:none; color:white;" href="mailto:webmaster@spdmizzou.org">webmaster@spdmizzou.org</a></p><div class="collumn1"><img src="MU_Stacked.png" height = 100px width=100px/></div></div>	<p id="footerText">"Engineering is difficult. Don' + "'t" + ' go through it alone." </p></div>';
	/* for readability 
		<div id ="footerWrapper">
			<div id="innerFooterWrapper">
			
				<div class="collumn1" >
					<img src="coat.png" height = 100px width=100px/>
				</div>
				<p id="collumn2">Contact For Organization: <br> beta-omicron@sigmaphidelta.org </p>
				<p id="collumn2">Contact For Recruitment: <br> sigphirecruitment@gmail.com </p>
				<p id = "collumn2"> Contact For Webmaster: <br>cjwgr5@mail.missouri.edu</p>
				<div class="collumn1">
					<img src="MU_Stacked.png" height = 100px width=100px/>
				</div>
				
			</div>
			<p id="footerText">"Engineering is difficult. Don't go through it alone." </p>
		</div>
	*/		
		$("#end").append(str);
	}

});