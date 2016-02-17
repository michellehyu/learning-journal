
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from learning_journal.models import Entry, User
engine = engine_from_config(registry.settings, 'sqlalchemy.')
Session = sessionmaker(bind=engine)
session = Session()
a =[]
new = Entry(title="1")
a.append(new)
new = Entry(title="2")
a.append(new)
new = Entry(title="4")
a.append(new)
new = Entry(title="3")
a.append(new)
new = Entry(title="5", body="adjfhajkdfhk")
a.append(new)
session.add_all(a)
session.commit()

u = User(name="m", password="123")
session.add(u)
session.commit()

b = Entry.all()
for e in b:
    print(e.title)
print("by_id")

c = Entry.by_id()
print(c.title)
