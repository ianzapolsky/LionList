/*
 * lionlist.js
 * javascript for LionList, mostly ajax form error handling for login,
 * registration, password reset, and account edit.
 * Ian Zapolsky (01/06/13)
*/

/* form handling for the login page */

var login = (function() {

  var uni_error = false;
  var password_error = false;

  var initModule = function () {

    $( '#uni' ).change(function() {
  
      var username = $( '#uni' ).val();

      $.ajax({
        url: '/account/ajax/is_username/'+username+'/',
        type: 'GET',
        async: true,
        dataType: 'json',
        success: function( data ) {
          if (data.msg === false) {
            $( '#uni-label' ).html('Invalid UNI');
            $( '#uni-div' ).removeClass('has-success');
            $( '#uni-div' ).addClass('has-error');
            uni_error = true;
          } else {
            $( '#uni-label' ).html('');
            $( '#uni-div' ).removeClass('has-error');
            $( '#uni-div' ).addClass('has-success');
            uni_error = false;
          }
        }
      });
    });

    $( '#password' ).change(function() {
        
      var username = $( '#uni' ).val();
      var password = $( '#password' ).val();

      $.ajax({
        url: '/account/ajax/is_valid_password/'+username+'/'+password+'/',
        type: 'GET',
        async: true,
        dataType: 'json',
        success: function( data ) {
          if (data.msg === false) {
            if (username === '') {
              $( '#password-label' ).html('Please enter your UNI');
            } else {
              $( '#password-label' ).html('Invalid password');
            }
            $( '#password-div' ).removeClass('has-success');
            $( '#password-div' ).addClass('has-error');
            password_error = true;
          } else {
            $( '#password-label' ).html('');
            $( '#password-div' ).removeClass('has-error');
            $( '#password-div' ).addClass('has-success');
            password_error = false;
          }
        }
      });
    });

    $( '#login-form' ).submit(function(event) {
      if ($( '#uni' ).val() === '') {
        $( '#uni-label' ).html('Please enter your UNI');
        $( '#uni-div' ).removeClass('has-success');
        $( '#uni-div' ).addClass('has-error');
        uni_error = true;
      }
      if ($( '#password' ).val() === '') {
        $( '#password-label' ).html('Please enter your password');
        $( '#password-div' ).removeClass('has-success');
        $( '#password-div' ).addClass('has-error');
        password_error = true;
      }
      if (uni_error === true || password_error === true) {
        event.preventDefault();
      }
    });

  };

  return { initModule : initModule };

}());

/* form handling for the registration page */

var registration = (function() {

  var uni_error = false;
  var password_error = false;
  var location_error = false;

  var initModule = function() {
  
    $( '#uni' ).change(function() {

      var username = $( '#uni' ).val();

      $.ajax({
        url: '/account/ajax/is_username/'+username+'/',
        type: 'GET',
        async: true,
        dataType: 'json',
        success: function( data ) {
          if (data.msg === true) {
            $( '#uni-label' ).html('A user with that UNI already exists');
            $( '#uni-div' ).removeClass('has-success');
            $( '#uni-div' ).addClass('has-error');
            uni_error = true;
          } else {
            $( '#uni-label' ).html('');
            $( '#uni-div' ).removeClass('has-error');
            $( '#uni-div' ).addClass('has-success');
            uni_error = false;
          }
        }
      });
    });

    $( '#password1, #password2' ).change(function() {

      var password1 = $( '#password1' ).val();
      var password2 = $( '#password2' ).val();

      $.ajax({
        url: '/account/ajax/validate_passwords/'+password1+'/'+password2+'/',
        type: 'GET',
        async: true,
        dataType: 'json',
        success: function( data ) {
          if (data.error === true) {
            $( '#password-label' ).html(data.msg);
            $( '#password-div' ).removeClass('has-success');
            $( '#password-div' ).addClass('has-error');
            password_error = true;
          } else {
            $( '#password-label' ).html('');
            $( '#password-div' ).removeClass('has-error');
            $( '#password-div' ).addClass('has-success');
            password_error = false;
          }
        }
      });
    });
  
    $( '#registration-form' ).submit(function(event) {
      if ($( '#uni' ).val() === '') {
        $( '#uni-label' ).html('Please enter your UNI');
        $( '#uni-div' ).removeClass('has-success');
        $( '#uni-div' ).addClass('has-error');
        uni_error = true;
      }
      if ($( '#password1' ).val() === '' || $( '#password2' ).val() === '') {
        $( '#password-label' ).html('Please enter and confirm your password');
        $( '#password-div' ).removeClass('has-success');
        $( '#password-div' ).addClass('has-error');
        password_error = true;
      }
      if ($( '#location' ).val() === 'empty') {
        $( '#location-label' ).html('Please enter your campus location');
        $( '#location-div' ).removeClass('has-success');
        $( '#location-div' ).addClass('has-error');
        location_error = true;
      }
      if (uni_error === true || password_error === true || location_error === true) {
        event.preventDefault();
      }
    });

  };

  return { initModule : initModule };

}());

/* form error handling for the edit account page */

var edit_account = (function() {

  var 
    current_password = false,
    password_present = false,
    password_error = false,
    email_present = false,
    email_error = false;
    form_error = false;
    
  var initModule = function() {

  $( '#password' ).change(function() {
    
    var 
      username = current_username,
      password = $( this ).val();

    $.ajax({
      url: '/account/ajax/is_valid_password/'+username+'/'+password+'/',
      type: 'GET',
      async: true,
      dataType: 'json',
      success: function( data ) {
        if (data.msg === false) {
          $( '#password-label' ).html('Invalid password');
          $( '#password-div' ).removeClass('has-success');
          $( '#password-div' ).addClass('has-error');
          current_password = false;
        } else {
          $( '#password-label' ).html('');
          $( '#password-div' ).removeClass('has-error');
          $( '#password-div' ).addClass('has-success');
          current_password = true;
        }
      }
    });
  });
  
  $( '#password1, #password2' ).change(function() {

    var password1 = $( '#password1' ).val();
    var password2 = $( '#password2' ).val();

    if (password1 === '' && password2 === '') {
      password_present = false;
      password_error = false;
      $( '#password1-label' ).html('');
      $( '#password1-div' ).removeClass('has-error');
      $( '#password1-div' ).removeClass('has-success');
    } 
  
    else {
      password_present = true;

      $.ajax({
        url: '/account/ajax/validate_passwords/'+password1+'/'+password2+'/',
        type: 'GET',
        async: true,
        dataType: 'json',
        success: function( data ) {
          if (data.error === true) {
            $( '#password1-label' ).html(data.msg);
            $( '#password1-div' ).removeClass('has-success');
            $( '#password1-div' ).addClass('has-error');
            password_error = true;
          } else {
            $( '#password1-label' ).html('');
            $( '#password1-div' ).removeClass('has-error');
            $( '#password1-div' ).addClass('has-success');
            password_error = false;
          }
        }
      });
    }

  });

  $( '#email' ).change(function() {

    var email = $( this ).val();

    if (email === '') {
      email_present = false;
      email_error = false;
      $( '#email-label' ).html('');
      $( '#email-div' ).removeClass('has-error');
      $( '#email-div' ).removeClass('has-success');
    }
    else {
    
    email_present = true;

    $.ajax({
      url: '/account/ajax/is_valid_email/'+email+'/',
      type: 'GET',
      async: true,
      dataType: 'json',
      success: function( data ) {
        if (data.error === true) {
          $( '#email-label' ).html(data.msg);
          $( '#email-div' ).removeClass('has-success');
          $( '#email-div' ).addClass('has-error');
          email_error = true;
        } else {
          $( '#email-label' ).html('');
          $( '#email-div' ).removeClass('has-error');
          $( '#email-div' ).addClass('has-success');
          email_error = false;
        }
      }
    });
    }
  });

  $( '#edit-form' ).change(function(event) {
  
    if ( $( '#password' ).val() === '') {
      $( '#form-label' ).html('Please enter your current password to make changes');
      form_error = true;
    }
    else if (password_present === false && email_present === false && 
             $( '#location' ).val() === 'empty') {
      $( '#form-label' ).html('You have not changed any information.');
      form_error = true;
    }
    else {
      $( '#form-label' ).html('');
      form_error = false;
    }
  });

  $( '#edit-form' ).submit(function(event) {
  
    if (current_password === false || password_error === true || 
        email_error === true || form_error === true) {
      event.preventDefault();
    }   
  });
 
  };

  return { initModule : initModule };

}());

/* form handling on the recover password page for forgotten passwords */

var recover_password = (function() {

  var uni_error = false;

  var initModule = function () {

    $( '#uni' ).change(function() {
  
      var username = $( '#uni' ).val();

      $.ajax({
        url: '/account/ajax/is_username/'+username+'/',
        type: 'GET',
        async: true,
        dataType: 'json',
        success: function( data ) {
          if (data.msg === false) {
            $( '#uni-label' ).html('Invalid UNI');
            $( '#uni-div' ).removeClass('has-success');
            $( '#uni-div' ).addClass('has-error');
            uni_error = true;
          } else {
            $( '#uni-label' ).html('');
            $( '#uni-div' ).removeClass('has-error');
            $( '#uni-div' ).addClass('has-success');
            uni_error = false;
          }
        }
      });
    });

    $( '#recovery-form' ).submit(function(event) {
      if ($( '#uni' ).val() === '') {
        $( '#uni-label' ).html('Please enter your UNI');
        $( '#uni-div' ).removeClass('has-success');
        $( '#uni-div' ).addClass('has-error');
        uni_error = true;
      }
      if (uni_error === true) {
        event.preventDefault();
      }
    });

  };
 
  return { initModule : initModule };

}());

/* form handling on the reset password page for forgotten passwords */

var reset_password = (function() {

   var password_error = false;

   var initModule = function() {

    $( '#password1, #password2' ).change(function() {

        var password1 = $( '#password1' ).val();
        var password2 = $( '#password2' ).val();

        $.ajax({
          url: '/account/ajax/validate_passwords/'+password1+'/'+password2+'/',
          type: 'GET',
          async: true,
          dataType: 'json',
          success: function( data ) {
            if (data.error === true) {
              $( '#password-label' ).html(data.msg);
              $( '#password-div' ).removeClass('has-success');
              $( '#password-div' ).addClass('has-error');
              password_error = true;
            } else {
              $( '#password-label' ).html('');
              $( '#password-div' ).removeClass('has-error');
              $( '#password-div' ).addClass('has-success');
              password_error = false;
            }
          }
        });
      });

      $( '#reset-form' ).submit(function(event) {
      if ($( '#password1' ).val() === '' || $( '#password2' ).val() === '') {
        $( '#password-label' ).html('Please enter and confirm your password');
        $( '#password-div' ).removeClass('has-success');
        $( '#password-div' ).addClass('has-error');
        password_error = true;
      }
      if (password_error === true) {
        event.preventDefault();
      }
    }); 
  };

  return { initModule : initModule };

}());
