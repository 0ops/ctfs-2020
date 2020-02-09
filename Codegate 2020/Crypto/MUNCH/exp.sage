p = 6880599843336662467879109387236213815987292188507187559989074121615354243311606616327703377828006351833629583392546362975490427453804091142854644316412663
seed = 6115683512551493681429013672578437250992709174507633110965073551143324876511315798363722262299405597781297506013981949713431316382568201987118489728973776

seed_inv = inverse_mod(seed, p)

reveal_data = [[365273572660559, 621483163501141, 273487816490195, 1075397252623564, 1914468910812945, 962961718578747, 420940837638395, 1573991110103234, 1841940053587716, 558893222798419, 1910717961955659, 1567996439899881, 868887510227897, 1314588757176622, 1693900629547647, 56234973351024, 1883177625103946, 2243764093782209, 1558555079410531, 1688483945377282, 1004362472376337, 578914720736828, 572175546886313, 920690743143218, 166099725703156, 2113704084012013, 1933991890191651, 1584350556327567, 689829581647088, 1014311704919724, 869728455696930, 475282365166640, 948325829047773, 316322757161915, 1133004743606733, 413251654097948, 551433636957783, 101282672877916, 1785440539579619, 2270407174853085, 676845953850845, 975035393647684, 2230572864819011, 1295962383729844, 1617286128325568, 372872018444, 1289460442319696, 2133121457298840, 63918446189908, 1691566118724085], [228957749427794, 1613904529954105, 151531815782072, 1505608634604579, 1449958424107745, 492775505618570, 769389932722088, 1400714164789778, 420575338863847, 1215393260436589, 422371988218178, 2193173496691391, 897432919933712, 1349424195128398, 1525267164169311, 1925918815506579, 246236676888424, 1077408515947411, 252098100710701, 1549666800062663, 1948808921789811, 1363465325184714, 340979809399667, 477941886516671, 2039256848643079, 2062092461008443, 1177925124477624, 593731528964815, 479369674173931, 754288839180058, 1864749572741264, 1547909564519771, 1454652268959382, 1213922549580749, 2151399978580323, 674423904166975, 920487928633848, 1231536851493911, 567403253985889, 1641168597532922, 2174753880306469, 527839506174836, 2111976384057693, 611323710580353, 928274387980042, 1788636647737738, 1750036145448962, 1186681523752311, 1114159378095436, 1615369417111975], [1023871873444793, 670371640095186, 1662852876327887, 349759022277267, 1708263912457545, 1449265435907005, 549881519479757, 581968837775620, 299279483936789, 1621782119801357, 1513263394020288, 566736180966973, 1419950508122052, 659859552921929, 1386373255161464, 287836215793395, 1944447510201202, 1138642240666237, 2239430963100067, 1464365625092491, 2031903620443744, 1433811139961805, 2171912600026334, 1774215443756664, 1454907268385438, 1614285283894297, 1686016253481693, 2083066020813294, 883198559498913, 1877376912607021, 1576512935738044, 1072200754479187, 413950997951054, 766210166059710, 1491074155967000, 1923710400363006, 2229216155425176, 817066453849768, 2026106354461017, 2289358538467132, 116625659234205, 409604259076605, 1010755791098506, 1599339020692593, 506796759542092, 1787946862093433, 2287699795049243, 535668657124933, 709574049560819, 960416212157945], [47252622313084, 746154892348423, 1698199163478340, 1134428317370092, 1608955265676391, 1077616772328631, 1676426597279872, 1376374167375553, 1186210612325224, 1320723047102254, 956317417537022, 81481592808825, 2253104843374582, 1240565365943525, 1536113899311190, 389246591225136, 608299716617507, 1751463533818637, 2135594922481591, 185536557129512, 2066731879678723, 1742483803193365, 1001051821134338, 1982565638845698, 1603061507691847, 759891517833802, 2209855994715577, 2067296679145133, 1884907467679494, 1823444794770617, 1920494272459775, 1447950537071799, 179876655529469, 2027301859734191, 374252276953386, 939078022522962, 1514460702803065, 1821037449806754, 148498723126041, 139429775743343, 1459734450825718, 405810742317469, 2249903249031774, 480416184280072, 1197623032961027, 491126743054673, 2068193669828051, 2157018791958130, 1320201392088036, 961170133381721]]

result = []
for j in range(4):
    Y = [i << 460 for i in reveal_data[j]]

    mat = []
    mat.append([p]+[0]*49)
    for i in range(1, 50):
        row = [0] * 50
        row[0] = pow(seed, 2**(4*i+j)-2**j, p).lift()
        row[i] = -1
        mat.append(row)
    L = matrix(mat)
    B = L.LLL()

    W1 = B * vector(Y)
    W2 = vector([ round(RR(w) / p) * p - w for w in W1 ])
    Z = list(B.solve_right(W2))
    X = list([0]*50)
    for i in range(50):
        X[i] = Y[i]+Z[i]

    tmp = X[0] * seed_inv**(2**j) % p
    result.append(tmp)

#print result

p0 = 10571149853133522431404264421866395513173821523643894835630672288391956736188404880335540994971314013670900609488503094055472955457681524945615744534010765
n = 123850820426090063939750639461336535800888872303996740868393788108622197265459429269747101462736954752274429639803614452794471290719054376275608856319222801843407104278834963103014930163521479153822223511859077469170499658852892275556238914610902748238728617276564375256445353397161395711740355127024574224311
enc = 56546264931253064991800011273062933350432906376123256400827688151463707024780705798157442404868856565703869323810835490194009709876675990770476983384812994742572992276677277260443081273365933217994869622952757076883760367020628026475789906867095354686131932884540071471310629032433408073596634685260647480557

x = 2916137381
y = 14174207518
z = 28127729793

p = p0 + x*(1<<111) + y*(1<<(146+111)) + z*(1<<(146*2+111))

assert n % p == 0

q = n / p
e = 65537
phi = (p-1)*(q-1)
d = inverse_mod(e, phi)

m = pow(enc,d,n).lift()

print m.hex().decode("hex")