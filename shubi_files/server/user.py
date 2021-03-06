import database as Database
import os
import random
from imagemanager import image_file_M


class User:
    @staticmethod
    def get_by_id(id):
        """Return image with specific id"""
        return Database.session.query(Database.Image).filter_by(id=id).first()

    @staticmethod
    def unselect(id=None):
        """Remove image from database selected"""
        if id is None:
            # delete all records
            Database.session.query(Database.Selected).delete()
        else:
            # delete specified id
            Database.session.query(Database.Selected).filter_by(image_id=id).delete()
        Database.commit()

    @staticmethod
    def select(id):
        """Add image to database selected"""
        exist = Database.session.query(Database.Selected).filter_by(image_id=id).first()
        if not exist:
            selected = Database.Selected(image_id=id)
            Database.session.add(selected)
            Database.commit()
        else:
            # image already selected
            pass

    @staticmethod
    def delete_selected():
        """Unselect every image"""
        Database.session.query(Database.Image).delete()
        Database.commit()

    @staticmethod
    def get_selected():
        return Database.session.query(Database.Image).join(Database.Selected).all()

    @staticmethod
    def add_uploaded(id, tags):

        if Database.session.query(Database.Uploaded).filter_by(image_id=id).first():
            Database.session.query(Database.Uploaded).filter_by(image_id=id).delete()
            img = Database.session.query(Database.Image).filter_by(id=id).first()
        else:
            # this image is already added. Lets change its tags.
            img = Database.session.query(Database.Image).filter_by(id=id).first()
            img.tags = []  # delete
        for tag in tags.split(','):
            # inspect tags
            tag = tag.strip().lower()
            if tag:
                if not Database.session.query(Database.Tag).filter_by(name=tag).first():
                    # tag not found
                    # creating new tag
                    Database.session.add(Database.Tag(name=tag))
                database_tag = Database.session.query(Database.Tag).filter_by(name=tag).first()
                img.tags.append(database_tag)
        Database.commit()

    @staticmethod
    def get_by_tag(tag):
        """

        :param tag: tag serching for
        :return: image path
        """
        tag = tag.strip()  # eliminate white spaces
        got = Database.session.query(Database.Image).filter(Database.Image.tags.any(name=tag)).order_by(
            Database.func.random())  # get random image with given tag
        # TODO: Emite sound
        try:
            if got:
                return got[0].file
        except IndexError:
            # image with this tage not found
            pass

    @staticmethod
    def get_uploaded():
        return (Database.session.query(Database.Image)
                .join(Database.Uploaded)).all()

    @staticmethod
    def delete(id):
        """Delete image with given id"""
        Database.session.query(Database.Uploaded).filter_by(image_id=id).delete()
        img = Database.session.query(Database.Image).filter_by(id=id).first()
        try:
            image_file_M.delete(img.file)
        except:
            print('File {} not found'.format(img.file))
        finally:
            Database.session.delete(img)
            Database.commit()

    @staticmethod
    def upload(images):
        """
        Add images to `uploaded` table
        :param images: dict with fields as in the database
        :return: ids of uploaded images
        """
        new_images = []
        uploaded = []
        for img in images:
            # kwarg unpacking might me risky. Should i do it?
            new_image = Database.Image(name=img['name'],
                                       original_name=img['original_name'],
                                       file=img['file'])
            new_images.append(new_image)
            # add it to uploaded database
            upload = Database.Uploaded(image=new_image)
            uploaded.append(upload)
        Database.session.add_all(new_images)
        Database.session.add_all(uploaded)

        Database.commit()
        return [image.id for image in new_images]

    @staticmethod
    def get_images():
        return (Database.session.query(Database.Image)
                .outerjoin(Database.Uploaded)
                .filter(Database.Uploaded.id == None)).all()


if __name__ == '__main__':
    x = User()
    x.unselect(1)


    # Get commong
    # SELECT * FROM selected
    # INNER JOIN images
    # ON images.id = selected.image_id

    # Get this in Images that are not in Selected
    # SELECT *
    # FROM images A
    # LEFT JOIN selected B
    # ON A.id = B.image_id
    # WHERE B.image_id IS NULL
