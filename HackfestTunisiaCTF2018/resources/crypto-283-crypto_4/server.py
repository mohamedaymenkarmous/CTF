from hashlib import sha256

SALT = "[REDACTED]"
FLAG = "[REDACTED]"

def register():
    usr = raw_input('Enter a username (max 9 characters): ')
    if(len(usr) > 9):
        print('The username is too long!')
        return
    key = sha256((SALT + usr)).hexdigest()
    token = usr.encode('hex') + ':' + key
    print("Here's your token:\n" + token)

def login():
    token = raw_input('Enter your token: ')
    usr, key = token.split(':')
    usr = usr.decode('hex')

    if(sha256((SALT + usr)).hexdigest() == key):
        print('Welcome ' + usr + '!')
        if('administrator' in usr):
            print("Here's the flag: " + FLAG)
        else:
            print('Nothing to see here :P')
    else:
        print('Invalid Token!')

def main():
    print('What do you want to do?')
    print('[1] Register')
    print('[2] Login')
    choice = raw_input('Enter your choice: ')

    if(choice == '1'):
        register()
    elif(choice == '2'):
        login()
    print('Closing connection.')        


if __name__ == '__main__':
    main()