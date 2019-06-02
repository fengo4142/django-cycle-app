$(document).ready(function() {

	//functional for navigation incon

	let nav_icon = $('.nav-icon'),
		account_bar = $('.account-bar'),
		general_form = $('.general_form');

		nav_icon.click(function(){
			account_bar.toggleClass('show'),
			general_form.toggleClass('show'),
			$(this).toggleClass('active');

			if($(this).hasClass('active')){
				$('body, html').css('overflow', 'hidden');
			}else(
				$('body, html').removeAttr('style')
			)
		})

	//dropdown list function

	$('.general_dropdown-list').each(function(){
		let that_list = $(this),
			that_span = that_list.find('span'),
			that_ul = that_list.find('ul');

			that_span.click(function(){
				that_ul.slideToggle();
				$(this).toggleClass('show')
			})
			that_ul.each(function(){
				let that_li = $(this).find('li');
				that_li.click(function(){
					let inner_content = $(this).text();
					that_ul.slideUp()
					that_span.text(inner_content).attr('data-name', inner_content).removeClass('show')
				})
			})
	})

	//input focus function
	$('body').on('focus', '.input_box input', function(){
		$(this).parent().addClass('focus')
	}).on('blur', '.input_box input', function(){
		if($(this).val() === ''){
			$(this).parent().removeClass('focus')
		}
	})

   $('select').each(function(){
				var $this = $(this), numberOfOptions = $(this).children('option').length;
			
				$this.addClass('select-hidden'); 
				$this.wrap('<div class="select"></div>');
				$this.after('<div class="select-styled"></div>');

				var $styledSelect = $this.next('div.select-styled');
				$styledSelect.text($this.children('option').eq(0).text());
			
				var $list = $('<ul />', {
						'class': 'select-options'
				}).insertAfter($styledSelect);
			
				for (var i = 0; i < numberOfOptions; i++) {
						$('<li />', {
								text: $this.children('option').eq(i).text(),
								rel: $this.children('option').eq(i).val()
						}).appendTo($list);
				}
			
				var $listItems = $list.children('li');
			
				$styledSelect.click(function(e) {
						e.stopPropagation();
						$('div.select-styled.active').not(this).each(function(){
								$(this).removeClass('active').next('ul.select-options').hide();
						});
						$(this).toggleClass('active').next('ul.select-options').toggle();
				});
			
				$listItems.click(function(e) {
						e.stopPropagation();
						$styledSelect.text($(this).text()).removeClass('active');
						$this.val($(this).attr('rel'));
						$list.hide();
						//console.log($this.val());
				});
			
				$(document).click(function() {
						$styledSelect.removeClass('active');
						$list.hide();
				});

		});



});


