#!/usr/bin/python3
"""A console to control Airbnb project"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
storage = FileStorage()


class HBNBCommand(cmd.Cmd):
    """contains the entry point of the command interpreter"""
    prompt = '(hbnb) '

    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def do_create(self, arg):
        """create a new instance of Basemodel,
        saves it to the Json file and prints the id"""
        if not arg:
            print("** class name missing **")
            return
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an
        instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        all_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        if key in all_objs:
            print(all_objs[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name
        and id
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        all_objs = storage.all()
        key = "{}.{}".format(class_name, instance_id)
        if key in all_objs:
            del all_objs[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of
        all instances based or not on the class name"""
        if '.' in arg:
            class_name, command = arg.split('.', 1)
            if command == "all()":
                if class_name in self.classes:
                    all_objs = storage.all(self.classes[class_name])
                    for obj in all_objs.values():
                        print(obj)
                else:
                    print("** class doesn't exist **")
        else:
            all_objs = storage.all()
            if not arg:
                for obj in all_objs.values():
                    print(obj)
                    return
            try:
                eval(arg)
            except NameError:
                print("** class doesn't exist **")
                return
            for obj in all_objs.values():
                if type(obj).__name__ == arg:
                    print(obj)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by
        adding or updating attribute (save the change into the
        JSON file)"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        try:
            eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        all_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        if key in all_objs:
            obj = all_objs[key]
            if args[2] not in ['id', 'created_at', 'updated_at']:
                value = args[3].strip('"')
                try:
                    value = eval(value)
                except NameError:
                    pass
                setattr(obj, args[2], value)
                storage.save()

        else:
            print("** no instance found **")

    def do_count(self, arg):
        """Counts the number of instances of class"""
        print(f"do_count method called with arg: {arg}")
        class_name = arg
        if class_name in self.classes:
            all_objs = storage.all()
            count = 0
            for obj in all_objs.values():
                if isinstance(obj, self.classes[class_name]):
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    def default(self, line):
        """Handle unrecognized commands"""
        if '.' in line and '(' in line and ')' in line:
            class_method, args = line.split('(')
            class_name, method_name = class_method.split('.', 1)
            args = args[:-1]  # Remove the closing ')'

            if method_name == "show":
                self.do_show(class_name + " " + args.strip('"'))
            elif method_name == "count":
                self.do_count(class_name)
            elif method_name == "destroy":
                self.do_destroy(class_name + " " + args.strip('"'))
            elif method_name == "update":
                self.do_update(args)
            else:
                self.do_all(class_name)
            return

        super().default(line)

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """An empty line + ENTER shouldn’t execute anything"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
