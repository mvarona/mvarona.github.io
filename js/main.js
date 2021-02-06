function printCurrentYear() {
	document.querySelector(".copy-current-year").innerHTML = "© " + new Date().getFullYear();
}

function updateBgc(){
	var velocity = 0.3;
	// var pos = $(window).scrollTop(); 
	// $('section').each(function() { 
	// 	var $element = $(this);
	// 	var height = $element.height()-18;
	// 	$(this).css('backgroundPosition', '50% ' + Math.round((height - pos) * velocity) + 'px'); 
	// });
}

function setUpScrollEffect(){
	$(window).bind('scroll', updateBgc);

	var movementStrength = 25;
	var height = movementStrength / $(window).height();
	var width = movementStrength / $(window).width();
	$("*").mousemove(function(e){
		var pageX = e.pageX - ($(window).width() / 2);
		var pageY = e.pageY - ($(window).height() / 2);
		var newvalueX = width * pageX * -1 - 25;
		var newvalueY = height * pageY * -1 - 50;
		$('section').css("background-position", newvalueX+"px     "+newvalueY+"px");
	});
}

function truncateMenuItems(){
	const MAX_LENGTH = 13;
	const items = document.querySelectorAll(".span-wrapper a");
	items.forEach(item => {
		if (item.innerHTML.length > MAX_LENGTH){
			item.innerHTML = item.innerHTML.slice(0, MAX_LENGTH) + "...";
		}
	});
}

function renderSkillsChart(){
	var ctx = document.getElementById('skills-chart').getContext('2d');
	var myChart = new Chart(ctx, {
	    type: 'horizontalBar',
	    data: {
	        labels: Object.keys(skillsData),
	        datasets: [{
	            label: '',
	            data: Object.values(skillsData),
	            backgroundColor: [
	                '#1abc9c',
	                '#16a085',
	                '#2ecc71',
	                '#27ae60',
	                '#3498db',
	                '#2980b9',
	                '#9b59b6',
	                '#8e44ad',
	                '#34495e',
	                '#2c3e50',
	                '#f1c40f',
	                '#f39c12',
	                '#e67e22',
	                '#d35400',
	                '#e74c3c',
	                '#c0392b',
	                '#ecf0f1',
	                '#bdc3c7',
	                '#95a5a6',
	                '#7f8c8d'
	            ],
	            borderColor: [
	                'rgba(75, 192, 192, 1)'
	            ],
	            borderWidth: 1
	        }]
	    },
	    options: {
	        scales: {
	            xAxes: [
            	{
	            	position: 'bottom',
	                ticks: {
	                	mirror: false,
	                	beginAtZero: true,
	                    callback: function(value, index, values) {
	                    	let lan = document.getElementsByTagName('html')[0].getAttribute('lang');
	                    	if (value == 0) {
	                    		return skillsLevelsStrings["insufficient_" + lan];
	                    	} else if (value == 50){
	                    		return skillsLevelsStrings["sufficient_" + lan];
	                    	} else if (value == 100){
	                    		return skillsLevelsStrings["excellent_" + lan];
	                    	}
	                    },
	                    fontColor: '#fff',
	                    fontSize: 16
	                }
	            }],
	            yAxes: [{
	            	ticks: {
	            		mirror: true,
	                    fontColor: '#fff',
	                    fontStyle: 'normal',
	                    fontSize: 15
	                }
	            }]
	        },
	        animation: {
			    onProgress () {
			      const chartInstance = this.chart;
			      const ctx = chartInstance.ctx;
			      const dataset = this.data.datasets[0];
			      const meta = chartInstance.controller.getDatasetMeta(0);

			      Chart.helpers.each(meta.data.forEach((bar, index) => {
			        const label = this.data.labels[index];
			        const labelPositionX = 90;
			        const labelWidth = ctx.measureText(label).width + labelPositionX;

			        ctx.textBaseline = 'middle';
			        ctx.textAlign = 'left';
			        ctx.font = "normal 15px Helvetica";
			        ctx.fillStyle = '#fff';
			        ctx.fillText(label, labelPositionX, bar._model.y);
			      }));
			    }
		  	},
		  	legend: {
			    display: false,
			      labels: {
			        display: false
			      }
		  	}
	    }
	});
}

function conditionalChartRendering(){
	var charts = document.querySelectorAll('#skills-chart');
	if (charts.length > 0){
		renderSkillsChart();
	}
}

function loadGalleryItem(index){
	$('.carousel').carousel(index);
}

function animateNumbers(){
	const animateCountUp = el => {
		const animationDuration = 1500;
		const frameDuration = 1000 / 60;
		const totalFrames = Math.round(animationDuration / frameDuration);
		const easeOutQuad = t => t * ( 2 - t );
		let frame = 0;
		const countTo = parseInt( el.innerHTML, 10 );
		const counter = setInterval( () => {
			frame++;
			const progress = easeOutQuad(frame / totalFrames );
			const currentCount = Math.round( countTo * progress );
			if (parseInt(el.innerHTML, 10) !== currentCount ) {
				el.innerHTML = currentCount;
			}
			if (frame === totalFrames) {
				clearInterval(counter);
			}
		}, frameDuration);
	};

	const runAnimations = () => {
		const countupEls = document.querySelectorAll('.animateNumber');
		countupEls.forEach(animateCountUp);
	};
	runAnimations();
}

function detectLanguage(){
	let userLang = navigator.language || navigator.userLanguage;

	var enURL;
	var esURL;
	var deURL;

	let navLinks = document.querySelectorAll('a.nav-link');
	navLinks.forEach(link => {
		if (link.innerHTML.toLowerCase() == "en"){
			enURL = link.href;
		} else if (link.innerHTML.toLowerCase() == "de"){
			deURL = link.href;
		} else if (link.innerHTML.toLowerCase() == "es"){
			esURL = link.href;
		}
	});

	let enDetected = "We think we have a better version for you! <a href='" + enURL + "'>Read this site in English</a>";
	let esDetected = "¡Creemos que tenemos una mejor versión para ti! <a href='" + esURL + "'>Lee este sitio en español</a>";
	let deDetected = "Wir denken, wir haben eine bessere Version für dich! <a href='" + deURL + "'>Lies diese Seite auf Deutsch</a>";

	let enLegalDetected = "We are sorry, the only legally binding version of these terms is the Spanish one";
	let deLegalDetected = "Es tut uns leid, die einzige rechtsverbindliche Version dieser Bedingungen ist die spanische";

	let url = window.location.href;
	let queryString = window.location.search;
	let urlParams = new URLSearchParams(queryString);
	let warning = document.querySelector('#lan-alert');
	let newElement = document.createElement('span');

	if (url.includes('/tos') || url.includes('/privacy')){

		if (urlParams.get('lan') == 'de'){
			newElement.innerHTML = deLegalDetected;
			warning.insertBefore(newElement, warning.firstChild);
			$('#lan-alert').delay(600).slideDown();
		}

		if (urlParams.get('lan') == 'en'){
			newElement.innerHTML = enLegalDetected;
			warning.insertBefore(newElement, warning.firstChild);
			$('#lan-alert').delay(600).slideDown();
		}

	} else {
		if (userLang.includes('es') && !url.includes('es/')){
			newElement.innerHTML = esDetected;
			warning.insertBefore(newElement, warning.firstChild);
			$('#lan-alert').delay(600).slideDown();
		} else if (userLang.includes('de') && !url.includes('de/')){
			newElement.innerHTML = deDetected;
			warning.insertBefore(newElement, warning.firstChild);$('#lan-alert').show();
			$('#lan-alert').delay(600).slideDown();
		} else if (userLang.includes('en') && !url.includes('en/')){
			newElement.innerHTML = enDetected;
			warning.insertBefore(newElement, warning.firstChild);
			$('#lan-alert').delay(600).slideDown();
		}
	}

}

function render404Page(){
	printCurrentYear();
	setUpScrollEffect();
	truncateMenuItems();
	let translations = {
		"error-404-title_en": "Error 404",
		"error-404-title_es": "Error 404",
		"error-404-title_de": "Fehler 404",
		"error-404-subtitle_en": "Oops, something went wrong",
		"error-404-subtitle_es": "Ups, algo fue mal",
		"error-404-subtitle_de": "Hoppla! Alles ist schiefgegangen",
		"error-404-desc_en": "We couldn't find what you were looking for.<br/>Please check if there is a typo in the address.<br/>If not, don't worry, I will work hard to make sure this doesn't happen again. In the meantime, you can always...",
		"error-404-desc_es": "No hemos conseguido encontrar lo que buscabas.<br/>Por favor, revisa si hay algún error en la dirección tecleada.<br/>En caso contrario, no te preocupes, trabajaré duro para que esto no se vuelva a producir. Mientras tanto, siempre puedes...",
		"error-404-desc_de": "Wir konnten nicht finden, wonach Sie gesucht haben.<br/>Bitte überprüfen Sie, ob es einen Tippfehler in der Adresse gibt.<br/>Wenn nicht, machen Sie sich keine Sorgen, ich werde hart arbeiten, um sicherzustellen, dass dies nicht wieder passiert. In der Zwischenzeit können Sie immer...",
		"error-404-sol-1_en": "Go back to home 🏡",
		"error-404-sol-1_es": "Volver al inicio 🏡",
		"error-404-sol-1_de": "Zurück zur Startseite gehen 🏡",
		"tos_en": "Terms of Use",
		"tos_es": "Términos de Uso",
		"tos_de": "Nutzungsbedingungen",
		"privacy_en": "Privacy Policy",
		"privacy_es": "Política de Privacidad",
		"privacy_de": "Datenschutzbestimmungen",
		"icons_cortesy_en": "Icons by <a href='https://www.icons8.com' target='_blank'>icons8.com</a>",
		"icons_cortesy_es": "Iconos de <a href='https://www.icons8.com' target='_blank'>icons8.com</a>",
		"icons_cortesy_de": "Icons durch <a href='https://www.icons8.com' target='_blank'>icons8.com</a>"
	};
	let url = window.location.href;
	let userLang = navigator.language || navigator.userLanguage; 
	var detectedLan = 'en';

	if (url.includes('404')){

		if (userLang.includes('es')){
			detectedLan = 'es';
		} else if (userLang.includes('de')){
			detectedLan = 'de'
			document.querySelector("nav li a[href='https://www.mariovarona.dev/es/index.html']").parentElement.classList.remove('active')
			document.querySelector("nav li a[href='https://www.mariovarona.dev/de/index.html']").parentElement.classList.add('active')
		} else {
			document.querySelector("nav li a[href='https://www.mariovarona.dev/en/index.html']").parentElement.classList.add('active')
		}

		document.getElementById('error-404-title').innerHTML = translations['error-404-title_' + detectedLan];
		document.getElementById('error-404-subtitle').innerHTML = translations['error-404-subtitle_' + detectedLan];
		document.getElementById('error-404-desc').innerHTML = translations['error-404-desc_' + detectedLan];
		document.getElementById('error-404-sol-1').innerHTML = translations['error-404-sol-1_' + detectedLan];

		document.getElementById('privacy').innerHTML = translations['privacy_' + detectedLan];
		document.getElementById('tos').innerHTML = translations['tos_' + detectedLan];
		document.getElementById('icons_cortesy').innerHTML = translations['icons_cortesy_' + detectedLan];
	}
}

function renderGeneralSettings(){
	printCurrentYear();
	setUpScrollEffect();
	truncateMenuItems();
	conditionalChartRendering();
	animateNumbers();
	detectLanguage();
}

$("#lan-alert").on("click", "button.close", function() {
	$(this).parent().slideUp(600).delay(1000).hide('slow');
});

$(document).ready(function() {
  $(".animsition").animsition({
    inClass: 'zoom-in-sm',
    outClass: 'zoom-out-sm',
    inDuration: 500,
    outDuration: 500,
    linkElement: '.animsition-link',
    loading: true,
    loadingParentElement: 'body',
    loadingClass: 'animsition-loading',
    loadingInner: '',
    timeout: true,
    timeoutCountdown: 0,
    onLoadEvent: true,
    browser: [],
    overlay : false,
    overlayClass : 'animsition-overlay-slide',
    overlayParentElement : 'body',
    transition: function(url){ window.location.href = url; }
  });
});