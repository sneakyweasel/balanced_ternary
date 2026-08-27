# Odd fourth-power successor search

Status: **COMPLETE**

Exact integer search for `T(n) = a^4` on odd non-square `n`.
A finite empty range is evidence, not a theorem.

## Range

- search_id: `juggler_odd_sharp_suffix-s2-odd-fourth-v1-cbrt-1-1000000`
- a-range: `[1, 1000000)`
- algorithm: `odd-fourth-v1-cbrt`
- arithmetic: `python-int`
- git: `4e201b7b9f636daa698eddcbe6c89cfc8f717465`
- checksum: `58707cec226bd95dc15ed74cd5cdf994ef2ce2a5680101d5c64118c40ffe1fc2`

## Counts

- candidates tested: `999999`
- interval cubes: `100`
- even cubes: `50`
- odd squares: `50`
- odd non-squares: `0`
- min gap: `40`
- max gap: `9223372036854775807`

## Smallest recorded cube

`{'hit_id': 1, 'chunk_id': 1, 's': 2, 'a': 1, 'n': '1', 'n_is_odd': 1, 'n_is_square': 1, 'exact_Tn': '1', 'interval_lower': '1', 'interval_upper': '4', 'cube_residual': '0', 'classification': 'ODD_SQUARE', 'n_mod_2': 1, 'n_mod_4': 1, 'n_mod_8': 1, 'n_mod_16': 1, 'a_mod_2': 1, 'a_mod_4': 1, 'a_mod_8': 1, 'a_mod_16': 1}`

## Strongest near miss

`{'miss_id': 1, 'chunk_id': 1, 'a': 2, 'side': 'lower', 'd': '40', 'm': None, 'kind': 'best_lower'}`

## Hits

- a `1`: n `1` ODD_SQUARE n_mod_16=`1` a_mod_16=`1`
- a `8`: n `256` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `27`: n `6561` ODD_SQUARE n_mod_16=`1` a_mod_16=`11`
- a `64`: n `65536` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `97`: n `198636` EVEN_CUBE n_mod_16=`12` a_mod_16=`1`
- a `125`: n `390625` ODD_SQUARE n_mod_16=`1` a_mod_16=`13`
- a `216`: n `1679616` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `343`: n `5764801` ODD_SQUARE n_mod_16=`1` a_mod_16=`7`
- a `512`: n `16777216` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `729`: n `43046721` ODD_SQUARE n_mod_16=`1` a_mod_16=`9`
- a `1000`: n `100000000` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `1331`: n `214358881` ODD_SQUARE n_mod_16=`1` a_mod_16=`3`
- a `1728`: n `429981696` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `2197`: n `815730721` ODD_SQUARE n_mod_16=`1` a_mod_16=`5`
- a `2744`: n `1475789056` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `3375`: n `2562890625` ODD_SQUARE n_mod_16=`1` a_mod_16=`15`
- a `4096`: n `4294967296` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `4913`: n `6975757441` ODD_SQUARE n_mod_16=`1` a_mod_16=`1`
- a `5832`: n `11019960576` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `6859`: n `16983563041` ODD_SQUARE n_mod_16=`1` a_mod_16=`11`
- a `8000`: n `25600000000` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `9261`: n `37822859361` ODD_SQUARE n_mod_16=`1` a_mod_16=`13`
- a `10648`: n `54875873536` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `12167`: n `78310985281` ODD_SQUARE n_mod_16=`1` a_mod_16=`7`
- a `13824`: n `110075314176` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `15625`: n `152587890625` ODD_SQUARE n_mod_16=`1` a_mod_16=`9`
- a `17576`: n `208827064576` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `19683`: n `282429536481` ODD_SQUARE n_mod_16=`1` a_mod_16=`3`
- a `21952`: n `377801998336` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `24389`: n `500246412961` ODD_SQUARE n_mod_16=`1` a_mod_16=`5`
- a `27000`: n `656100000000` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `29791`: n `852891037441` ODD_SQUARE n_mod_16=`1` a_mod_16=`15`
- a `32768`: n `1099511627776` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `35937`: n `1406408618241` ODD_SQUARE n_mod_16=`1` a_mod_16=`1`
- a `39304`: n `1785793904896` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `42875`: n `2251875390625` ODD_SQUARE n_mod_16=`1` a_mod_16=`11`
- a `46656`: n `2821109907456` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `50653`: n `3512479453921` ODD_SQUARE n_mod_16=`1` a_mod_16=`13`
- a `54872`: n `4347792138496` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `59319`: n `5352009260481` ODD_SQUARE n_mod_16=`1` a_mod_16=`7`
- a `64000`: n `6553600000000` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `68921`: n `7984925229121` ODD_SQUARE n_mod_16=`1` a_mod_16=`9`
- a `74088`: n `9682651996416` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `79507`: n `11688200277601` ODD_SQUARE n_mod_16=`1` a_mod_16=`3`
- a `85184`: n `14048223625216` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `91125`: n `16815125390625` ODD_SQUARE n_mod_16=`1` a_mod_16=`5`
- a `97336`: n `20047612231936` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `103823`: n `23811286661761` ODD_SQUARE n_mod_16=`1` a_mod_16=`15`
- a `110592`: n `28179280429056` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `117649`: n `33232930569601` ODD_SQUARE n_mod_16=`1` a_mod_16=`1`
- a `125000`: n `39062500000000` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `132651`: n `45767944570401` ODD_SQUARE n_mod_16=`1` a_mod_16=`11`
- a `140608`: n `53459728531456` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `148877`: n `62259690411361` ODD_SQUARE n_mod_16=`1` a_mod_16=`13`
- a `157464`: n `72301961339136` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `166375`: n `83733937890625` ODD_SQUARE n_mod_16=`1` a_mod_16=`7`
- a `175616`: n `96717311574016` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `185193`: n `111429157112001` ODD_SQUARE n_mod_16=`1` a_mod_16=`9`
- a `195112`: n `128063081718016` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `205379`: n `146830437604321` ODD_SQUARE n_mod_16=`1` a_mod_16=`3`
- a `216000`: n `167961600000000` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `226981`: n `191707312997281` ODD_SQUARE n_mod_16=`1` a_mod_16=`5`
- a `238328`: n `218340105584896` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `250047`: n `248155780267521` ODD_SQUARE n_mod_16=`1` a_mod_16=`15`
- a `262144`: n `281474976710656` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `274625`: n `318644812890625` ODD_SQUARE n_mod_16=`1` a_mod_16=`1`
- a `287496`: n `360040606269696` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `300763`: n `406067677556641` ODD_SQUARE n_mod_16=`1` a_mod_16=`11`
- a `314432`: n `457163239653376` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `328509`: n `513798374428641` ODD_SQUARE n_mod_16=`1` a_mod_16=`13`
- a `343000`: n `576480100000000` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `357911`: n `645753531245761` ODD_SQUARE n_mod_16=`1` a_mod_16=`7`
- a `373248`: n `722204136308736` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `389017`: n `806460091894081` ODD_SQUARE n_mod_16=`1` a_mod_16=`9`
- a `405224`: n `899194740203776` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `421875`: n `1001129150390625` ODD_SQUARE n_mod_16=`1` a_mod_16=`3`
- a `438976`: n `1113034787454976` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `456533`: n `1235736291547681` ODD_SQUARE n_mod_16=`1` a_mod_16=`5`
- a `474552`: n `1370114370683136` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `493039`: n `1517108809906561` ODD_SQUARE n_mod_16=`1` a_mod_16=`15`
- a `512000`: n `1677721600000000` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `531441`: n `1853020188851841` ODD_SQUARE n_mod_16=`1` a_mod_16=`1`
- a `551368`: n `2044140858654976` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `571787`: n `2252292232139041` ODD_SQUARE n_mod_16=`1` a_mod_16=`11`
- a `592704`: n `2478758911082496` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `614125`: n `2724905250390625` ODD_SQUARE n_mod_16=`1` a_mod_16=`13`
- a `636056`: n `2992179271065856` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `658503`: n `3282116715437121` ODD_SQUARE n_mod_16=`1` a_mod_16=`7`
- a `681472`: n `3596345248055296` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `704969`: n `3936588805702081` ODD_SQUARE n_mod_16=`1` a_mod_16=`9`
- a `729000`: n `4304672100000000` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `753571`: n `4702525276151521` ODD_SQUARE n_mod_16=`1` a_mod_16=`3`
- a `778688`: n `5132188731375616` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `804357`: n `5595818096650401` ODD_SQUARE n_mod_16=`1` a_mod_16=`5`
- a `830584`: n `6095689385410816` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `857375`: n `6634204312890625` ODD_SQUARE n_mod_16=`1` a_mod_16=`15`
- a `884736`: n `7213895789838336` EVEN_CUBE n_mod_16=`0` a_mod_16=`0`
- a `912673`: n `7837433594376961` ODD_SQUARE n_mod_16=`1` a_mod_16=`1`
- a `941192`: n `8507630225817856` EVEN_CUBE n_mod_16=`0` a_mod_16=`8`
- a `970299`: n `9227446944279201` ODD_SQUARE n_mod_16=`1` a_mod_16=`11`

