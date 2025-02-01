# fennálló probléma

- a regisztráció sikeres
- a gondok a bejelentkezéssel "vannak"...
  - azaz a bejelentkezési adatok helyesek, de a bejelentkezés nem sikerül (401-es hibakód)
  - szinte teljesen biztos, hogy a probléma forrása a `token` körül keresendő
  - miért gondolom ezt?
    --- 
    - mert nem találom a `token`-t a `localStorage`-ban

~~~
a Swagger UI-t használtam a teszteléshez
regisztráltam
beléptem
hoztam létre új jegyzetet
lekérdeztem
...

aztán hozzáadtam a hitelesítést,
hogy kizárólag bejelentkezve lehessen elérni a jegyzeteket,
és itt kezdődtek a gondok...

amennyiben bejelentkezem, és nincs hitelesítés-ellenőrzés,
akkor, pl az 1-es felhasználóval lekért:
http://localhost:8000/notes/1
csak akkor működik, ha:
http://localhost:8000/notes/1?token={token}
és a token elérhető a Swagger UI-ban
~~~

érdekes. nem?

mivel már lejárt az idő, így ez így marad...
kis pihenés után arra gondoltam, hogy lehet, hogy csomagprobléma van...
több csomag is eléggé módosításra került, mióta utoljára használtam, és mi a garancia arra, hogy minden friss verzió csak javításokat és újításokat tartalmaz?
