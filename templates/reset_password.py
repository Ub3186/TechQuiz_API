def reset_password_html():
    return '''
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap"
        rel="stylesheet">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Forget Password</title>

    <style>
        *,
        *::after,
        *::before {
            margin: 0;
            padding: 0;
        }

        body {
            margin: .5em;
            font-family: 'Roboto', sans-serif;
            background-color: #eee;
            display: flex;
            justify-content: center;
            align-content: center;
        }

        a {
            text-decoration: none;
        }

        p {
            margin: 1em 0;
        }

        form {
            margin-top: 1em;
        }

        label {
            display: block;
            margin: .5em 0;
        }

        input {
            margin: .5em 0;
            padding: .5em;
        }

        .container {
            background-color: white;
            margin-top: 5em;
            padding: 2em;
            border-radius: 5px;
        }

        .resetbtn {
            display: block;
            margin: .5em 0;
            padding: 1em;
            border-radius: 5px;
            background-color: black;
            color: white;
        }

        .regards {
            font-weight: 100;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>Techquiz password reset</h1>
        <form>
            <label for="password">New Password</label>
            <input name="password" class="password" type="password" required />

            <label for="confirmPassword">Re-type Password</label>
            <input name="confirmPassword" class="confirm" type="password" required />
            
            <input type="submit" value="Submit" class="resetbtn">
        </form>
        <p class="text"></p>
    </div>

    <script>
        let text = document.querySelector(".text")
        document.querySelector(".password").addEventListener('click', (e) => {
            text.textContent = " "
        })

        document.querySelector(".resetbtn").addEventListener('click', async (e) => {
            e.preventDefault()
            
            let email = (location.pathname+location.search).substr(1).replace("reset_password/","")
            let password = document.querySelector(".password").value
            let confirmPassword = document.querySelector(".confirm").value

            text.value = " "

            if(password.length < 7 || confirmPassword < 7){
                return text.textContent = "Password length needs to be greater than 6 characters"
            }

            if(password != confirmPassword){
                return text.textContent = "Password dosen't match"
            }

            var myHeaders = new Headers();
            myHeaders.append("Content-Type", "application/json");

            var raw = JSON.stringify({
                "email": email,
                "password": password
            });

            var requestOptions = {
                method: 'PATCH',
                headers: myHeaders,
                body: raw,
                redirect: 'follow'
            };

            fetch("https://techquiz-api.herokuapp.com/update_password", requestOptions)
                .then(response => response.json())
                .then(result => {
                    if(result.error){
                        return text.textContent = result.error
                    }

                    text.textContent = "Succesfully updated password"
                })
                .catch(error => console.log('error', error));
        })
    </script>
</body>

</html>
    '''
