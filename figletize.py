#!/usr/local/bin/python3
########################################
# Turn some text into ascii art
# v0.0.1 3Oct2014
#
# Basically the pretty engine of my radio client
#
if __name__=="__main__":
	USAGE = """
Usage %s -f <font> -s <string>
\t--help\tThis help message
\t--font\tFont to use
\t--str\tString to pyfigletize


Command line wrapper for pyfiglet.
Changing strings into ascii art banners.
"""
# end if main, continues again towards bottom of code
#
# TODO
#
##### Dependencies that you might need to install
# pyfiglet
import sys      # for argv and exit
import random   # only needed if you don't specify a font
import getopt   # for parsing the args
import pyfiglet # why we're here

# built-in font fetch doesn't work:
#fonts = f.getFonts ()
#for font in fonts:
#    print ("font: " + font)
#.../pyfiglet-master $ ls -l pyfiglet/fonts/ | grep -v '^total' | grep -v py$ | sed -e "s/.*:33 /, '/" | sed  -e "s/_*.flf.*/'/" | paste -s -d" " -
# Below is all the possible fonts that you could choose:
"""
fonts = ['1943' , '3-d' , '3x5' , '4x4_offr' , '5lineoblique' , '5x7' , '64f1' , '6x10' , '6x9' , 'a_zooloo' , 'acrobatic' , 'advenger' , 'alligator' , 'alligator2' , 'alphabet' , 'aquaplan' , 'ascii' , 'assalt_m' , 'asslt__m' , 'atc' , 'atc_gran' , 'avatar' , 'banner' , 'banner3-D' , 'banner3' , 'banner4' , 'barbwire' , 'basic' , 'battle_s' , 'battlesh' , 'baz__bil' , 'beer_pub' , 'bell' , 'big' , 'bigchief' , 'binary' , 'block' , 'brite' , 'briteb' , 'britebi' , 'britei' , 'broadway' , 'bubble' , 'bubble' , 'bubble_b' , 'bulbhead' , 'c1' , 'c2' , 'c_ascii' , 'c_consen' , 'calgphy2' , 'caligraphy' , 'catwalk' , 'caus_in' , 'char1' , 'char2' , 'char3' , 'char4' , 'charact1' , 'charact2' , 'charact3' , 'charact4' , 'charact5' , 'charact6' , 'characte' , 'charset' , 'chartr' , 'chartri' , 'chunky' , 'clb6x10' , 'clb8x10' , 'clb8x8' , 'cli8x8' , 'clr4x6' , 'clr5x10' , 'clr5x6' , 'clr5x8' , 'clr6x10' , 'clr6x6' , 'clr6x8' , 'clr7x10' , 'clr7x8' , 'clr8x10' , 'clr8x8' , 'coil_cop' , 'coinstak' , 'colossal' , 'com_sen' , 'computer' , 'contessa' , 'contrast' , 'convoy' , 'cosmic' , 'cosmike' , 'cour' , 'courb' , 'courbi' , 'couri' , 'crawford' , 'cricket' , 'cursive' , 'cyberlarge' , 'cybermedium' , 'cybersmall' , 'd_dragon' , 'dcs_bfmo' , 'decimal' , 'deep_str' , 'demo_1' , 'demo_2' , 'demo_m' , 'devilish' , 'diamond' , 'digital' , 'doh' , 'doom' , 'dotmatrix' , 'double' , 'drpepper' , 'druid' , 'dwhistled' , 'e__fist' , 'ebbs_1' , 'ebbs_2' , 'eca' , 'eftichess' , 'eftifont' , 'eftipiti' , 'eftirobot' , 'eftitalic' , 'eftiwall' , 'eftiwater' , 'epic' , 'etcrvs' , 'f15' , 'faces_of' , 'fair_mea' , 'fairligh' , 'fbr12' , 'fbr1' , 'fbr2' , 'fbr_stri' , 'fbr_tilt' , 'fender' , 'finalass' , 'fireing' , 'flyn_sh' , 'fourtops' , 'fp2' , 'fraktur' , 'funky_dr' , 'future_1' , 'future_2' , 'future_3' , 'future_4' , 'future_5' , 'future_6' , 'future_7' , 'future_8' , 'fuzzy' , 'gauntlet' , 'ghost_bo' , 'goofy' , 'gothic' , 'gothic' , 'graceful' , 'gradient' , 'graffiti' , 'grand_pr' , 'green_be' , 'hades' , 'heavy_me' , 'helv' , 'helvb' , 'helvbi' , 'helvi' , 'heroboti' , 'hex' , 'high_noo' , 'hills' , 'hollywood' , 'home_pak' , 'house_of' , 'hypa_bal' , 'hyper' , 'inc_raw' , 'invita' , 'isometric1' , 'isometric2' , 'isometric3' , 'isometric4' , 'italic' , 'italics' , 'ivrit' , 'jazmine' , 'jerusalem' , 'joust' , 'kban' , 'kgames_i' , 'kik_star' , 'krak_out' , 'larry3d' , 'lazy_jon' , 'lcd' , 'lean' , 'letter_w' , 'letters' , 'letterw3' , 'linux' , 'lockergnome' , 'mad_nurs' , 'madrid' , 'magic_ma' , 'marquee' , 'master_o' , 'maxfour' , 'mayhem_d' , 'mcg' , 'mig_ally' , 'mike' , 'mini' , 'mirror' , 'mnemonic' , 'modern' , 'morse' , 'moscow' , 'mshebrew210' , 'nancyj-fancy' , 'nancyj-underlined' , 'nancyj' , 'new_asci' , 'nfi1' , 'nipples' , 'notie_ca' , 'ntgreek' , 'nvscript' , 'o8' , 'octal' , 'odel_lak' , 'ogre' , 'ok_beer' , 'os2' , 'p_s_h_m' , 'p_skateb' , 'pacos_pe' , 'panther' , 'pawn_ins' , 'pawp' , 'peaks' , 'pebbles' , 'pepper' , 'phonix' , 'platoon2' , 'platoon' , 'pod' , 'poison' , 'puffy' , 'pyramid' , 'r2-d2' , 'rad' , 'rad_phan' , 'radical' , 'rainbow' , 'rally_s2' , 'rally_sp' , 'rastan' , 'raw_recu' , 'rci' , 'rectangles' , 'relief' , 'relief2' , 'rev' , 'ripper!' , 'road_rai' , 'rockbox' , 'rok' , 'roman' , 'roman' , 'rot13' , 'rounded' , 'rowancap' , 'rozzo' , 'runic' , 'runyc' , 'sans' , 'sansb' , 'sansbi' , 'sansi' , 'sblood' , 'sbook' , 'sbookb' , 'sbookbi' , 'sbooki' , 'script' , 'script' , 'serifcap' , 'shadow' , 'short' , 'skate_ro' , 'skateord' , 'skateroc' , 'sketch_s' , 'slant' , 'slide' , 'slscript' , 'sm' , 'small' , 'smisome1' , 'smkeyboard' , 'smscript' , 'smshadow' , 'smslant' , 'smtengwar' , 'speed' , 'stacey' , 'stampatello' , 'standard' , 'star_war' , 'starwars' , 'stealth' , 'stellar' , 'stencil1' , 'stencil2' , 'stop' , 'straight' , 'street_s' , 'subteran' , 'super_te' , 't__of_ap' , 'tanja' , 'tav1' , 'taxi' , 'tec1' , 'tec_7000' , 'tecrvs' , 'tengwar' , 'term' , 'thick' , 'thin' , 'threepoint' , 'ti_pan' , 'ticks' , 'ticksslant' , 'times' , 'timesofl' , 'tinker-toy' , 'tomahawk' , 'tombstone' , 'top_duck' , 'trashman' , 'trek' , 'triad_st' , 'tsalagi' , 'tsm' , 'tsn_base' , 'tty' , 'ttyb' , 'twin_cob' , 'twopoint' , 'type_set' , 'ucf_fan' , 'ugalympi' , 'unarmed' , 'univers' , 'usa' , 'usa_pq' , 'usaflag' , 'utopia' , 'utopiab' , 'utopiabi' , 'utopiai' , 'vortron' , 'war_of_w' , 'weird' , 'whimsy' , 'xbrite' , 'xbriteb' , 'xbritebi' , 'xbritei' , 'xchartr' , 'xchartri' , 'xcour' , 'xcourb' , 'xcourbi' , 'xcouri' , 'xhelv' , 'xhelvb' , 'xhelvbi' , 'xhelvi' , 'xsans' , 'xsansb' , 'xsansbi' , 'xsansi' , 'xsbook' , 'xsbookb' , 'xsbookbi' , 'xsbooki' , 'xtimes' , 'xtty' , 'xttyb' , 'yie-ar' , 'yie_ar_k' , 'z-pilot' , 'zig_zag']
nerdy_but_unpretty = [ 'hex' , 'octal' , 'binary' , 'rot13', 'morse' ]
"""


def randFont ():
	""" Uses an internal array of font options to choose and init a pyfiglet obj """
	# alot of the fonts are repeats or just unattactive,
	# here are the fonts that I find the most interesting:
	fonts = [ '3-d' , '3x5' , '5lineoblique' , 'a_zooloo' , 'acrobatic' , 'alligator' , 'alligator2' , 'alphabet' , 'avatar' , 'banner' , 'banner3-D' , 'banner4' , 'barbwire' , 'basic' , 'bell' , 'big' , 'bigchief' , 'block' , 'britebi' , 'broadway' , 'bubble' , 'bulbhead' , 'calgphy2' , 'caligraphy' , 'catwalk' , 'charact1' , 'charact4' , 'chartri' , 'chunky' , 'clb6x10' , 'coinstak' , 'colossal' , 'computer' , 'contessa' , 'contrast' , 'cosmic' , 'cosmike' , 'courbi' , 'crawford' , 'cricket' , 'cursive' , 'cyberlarge' , 'cybermedium' , 'cybersmall' , 'devilish' , 'diamond' , 'digital' , 'doh' , 'doom' , 'dotmatrix' , 'double' , 'drpepper' , 'dwhistled' , 'eftichess' , 'eftifont' , 'eftipiti' , 'eftirobot' , 'eftitalic' , 'eftiwall' , 'eftiwater' , 'epic' , 'fender' , 'fourtops' , 'fraktur' , 'funky_dr' , 'fuzzy' , 'goofy' , 'gothic' , 'graceful' , 'graffiti' , 'helvbi' , 'hollywood' , 'home_pak' , 'invita' , 'isometric1' , 'isometric2' , 'isometric3' , 'isometric4' , 'italic' , 'ivrit' , 'jazmine' , 'jerusalem' , 'kban' , 'larry3d' , 'lean' , 'letters' , 'linux' , 'lockergnome' , 'madrid' , 'marquee' , 'maxfour' , 'mike' , 'mini' , 'mirror' , 'moscow' , 'mshebrew210' , 'nancyj-fancy' , 'nancyj-underlined' , 'nancyj' , 'new_asci' , 'nipples' , 'ntgreek' , 'nvscript' , 'o8' , 'odel_lak' , 'ogre' , 'os2' , 'pawp' , 'peaks' , 'pebbles' , 'pepper' , 'poison' , 'puffy' , 'rectangles' , 'relief' , 'relief2' , 'rev' , 'roman', 'rounded' , 'rowancap' , 'rozzo' , 'runic' , 'runyc' , 'sansbi' , 'sblood' , 'sbookbi' , 'script' , 'serifcap' , 'shadow' , 'short' , 'sketch_s' , 'slant' , 'slide' , 'slscript' , 'small' , 'smisome1' , 'smkeyboard' , 'smscript' , 'smshadow' , 'smslant' , 'smtengwar' , 'speed' , 'stacey' , 'stampatello' , 'standard' , 'starwars' , 'stellar' , 'stop' , 'straight' , 't__of_ap' , 'tanja' , 'tengwar' , 'thick' , 'thin' , 'threepoint' , 'ticks' , 'ticksslant' , 'tinker-toy' , 'tombstone' , 'trek' , 'tsalagi' , 'twin_cob' , 'twopoint' , 'univers' , 'usaflag' , 'utopiabi' , 'weird' , 'whimsy' , 'xbritebi' , 'xcourbi']
	# do 100 tries in case font doesn't exist
	# if there are 100 failures, asciiArtText will fail/barf on its Figlet constructor
	for i in range (100):
		fi = fonts[random.randint (0, len (fonts) - 1)]
		#print (fi)
		try:
			f = pyfiglet.Figlet (font=fi)
		except:
			continue
		break
	#print (f.renderText (fi) )
	#fi = "bulbhead"
	return fi
	

def asciiArtText (str, font, term_w):
	""" Given a str, and a font (or rand for choose a font at random) and a terminal width. Returns figletized text and the font that was used. """
	# default is no figlets
	out = "\n" + str + "\n" + '-' * len (str) + "\n"
	if font != "rand":
		f = pyfiglet.Figlet (font=font)
		out = f.renderText (str) 
		return (out, font)
	else:
		# do 100 attempts to find a suitable font
		# criteria:
		#   must be narrower than term window
		#   wider than 1/4 the term window (the larger, the prettier)
		fi = "none"
		for i in range (100):
			fi = randFont ()
			f = pyfiglet.Figlet (font=fi) #, width=term_w )
			out = f.renderText (str) 
			from io import StringIO
			out_IO = StringIO (out)
			out_width = max([len (a) for a in out_IO.readlines ()])
			#print ("outWidth: %d"%outWidth)
			if out_width <= term_w and out_width > (term_w / 4):
				#print ("Font name: " + fi)
				return (out, fi)
	return (out, fi)

	 
def resetDimensions ():
	""" Get the terminal dimensions """
	try:
		# *nix get terminal/console width
		import os
		rows, columns = os.popen ('stty size', 'r').read().split()
		width  = int (columns)
		height = int (rows)
		return (width, height)
		#print ("term width: %d"% width)
	except:
		return (80, 40)
			

def usage ():
	""" If __main__ be able to show the usage """
	print (USAGE%sys.argv[0]) # uses the global from up top of this file
	(term_w, term_h) = resetDimensions ()
	(banner, font) = asciiArtText ("ASCII Art, FTW!", "rand", term_w)
	print (banner)
	print ("Font: " + font)
	sys.exit (0)
	



###################################
# main
if __name__=="__main__":
	try: 
		opts, args = getopt.getopt (sys.argv[1:], "hf:s:t:b:", ["help","font=","str=","txt=","banner="])
	except: 
		usage ()
	font = "rand"
	in_str = "test"
	for opt, arg in opts:
		# you can specify the specific font to use if you know the name
		if opt in ("-f", "--font"):
			font = arg
		# allows you to use s or b or t to specify the text to figletize
		elif opt in ("-s", "--str") or opt in ("-t", "--txt") or opt in ("-b", "--banner"):
			in_str = arg
		elif opt in ("-h", "--help"):
			usage ()
		else:
			usage ()
		  
	#######
	# do the deed in a loop until the user exits
	while (1):
		(term_w, term_h) = resetDimensions ()
		(banner, font) = asciiArtText (in_str, font, term_w)
		print (banner + '\n')
		print ("Font: " + font)
		ctrl_char = input ("Enter q to quit, or any key to show another font ")
		if (ctrl_char != "" and (ctrl_char[0].lower() == 'q' or ctrl_char[0].lower() == 'e')):
			sys.exit (0)
		font = "rand"
	# end while
# end main

# end .py
