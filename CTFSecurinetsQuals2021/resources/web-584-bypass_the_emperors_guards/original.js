function getRndInteger(min, max) {
  return Math.floor(Math.random() * (max - min + 1) ) + min;
}
var guards=[
'Securinets{Dunno where is the real flag ¯\_(ツ)_/¯}',
'Securinets{How you doin? ( ͡~ ͜ʖ ͡°)}',
'Securinets{I love how you\'re struggling to get the flag but you\'re stuck with me ٩(*❛⊰❛)～❤}',
'Securinets{Don\'t ask me please, I was forced to work as TheEmperor\'s guard ﴾͡๏̯͡๏﴿ }',
'Securinets{Am I pretty as TheEmperor\'s guard? ✧♡(◕‿◕✿)}',
'Securinets{Who are you? โ๏௰๏ใ ื}',
'Securinets{Hi? (ㆆ _ ㆆ)}',
'Securinets{I don\'t want to work in this stinky place \'(ᗒᗣᗕ)՞}',
'Securinets{Am I kawaiiii ? (◍＞◡＜◍)⋈。✧♡}',
'Securinets{Are you an angel? Or was this love at first sight? (ღ˘⌣˘)♥ ℒ♡ⓥℯ ㄚ♡ⓤ}',
'Securinets{I\'m really happy that I was promoted as one of TheEmperor\'s guards (♡´౪`♡)}',
'Securinets{Nyan ∩｡• ᵕ •｡∩ ♡}',
'Securinets{... That\'s why I wanted to ask you. Would you marry me? ( ° ᴗ°)~ð (/❛o❛\\)}',
'Securinets{I love you, (kissing voice) (>^o^)><(^o^<)}',
'Securinets{Free huuuuugs! ♥(ˆ⌣ˆԅ)}',
'Securinets{Mmmmmmouah (kissing voice) (• ε •)}',
'Securinets{Sooooo cute (kissing voice) ( ͡°❥ ͡°)}',
'Securinets{I love you soooo much (whispering with kissing voice) (っ˘з(˘⌣˘ )}',
'Securinets{I\'ll say it again and again, I love you (๑′ᴗ‵๑)Ｉ Lᵒᵛᵉᵧₒᵤ♥}',
'Securinets{I\'m cute as TheEmperor\'s guard ( ๑ ❛ ڡ ❛ ๑ )❤}',
'Securinets{I\'m the cutest TheEmperor\'s guard ╰(✿´⌣`✿)╯♡}',
'Securinets{Nighty night, I\'ll be guarding TheEmperor alone from now (ㅅꈍ﹃ꈍ)*gᵒᵒᒄ ᵑⁱgᑋᵗ♡(ꈍ﹃ꈍㅅ)*}',
'Securinets{Hi there, this is a restricted zone guarded for TheEmperor\'s safety. Please go in that direction(◟ᅇ)◜}',
'Securinets{Mah maaaan, are you ready???? (☞ﾟ∀ﾟ)☞}',
'Securinets{I\'m soooo strong to protect TheEmperor (╯°o°)ᕗ}',
'Securinets{It\'s about teamwork. We will be guarding TheEmperor whenever, wherever, forever and ever (\'_\')┏oo┓(\'_\')}',
'Securinets{Hey what the hell are you doing here? get back to where you come from. This place is guarded by TheEmperor\'s guards ┌( ಠ_ಠ)┘}',
'Securinets{I don\'t know what I\'m doing here as TheEmperor\'s guard 乁( ⁰͡ Ĺ̯ ⁰͡ ) ㄏ}',
'Securinets{Hmmmm well you know I\'m one of TheEmperor\'s guard ¯\_( ͡° ͜ʖ ͡°)_/¯}',
'Securinets{Yeaaaaaah ヽ(゜～゜o)ノ}',
'Securinets{Dunno, you can ask TheEmperor itself. Wait! I\'m TheEmperor\'s guard so you should not meet him v( ‘.’ )v}',
'Securinets{Pika Pika! ｡◕‿‿◕｡ 🗲}',
'Securinets{Purrrrrrrrrr 【≽ܫ≼】}',
'Securinets{Nyan ฅ^•ﻌ•^ฅ}',
'Securinets{You know what I mean ( ͡° ͜ʖ ͡°)}',
'Securinets{Well, I can be happy since I\'m one of TheEmperor\'s guards ˙ ͜ʟ˙}',
'Securinets{Please don\'t say that I\'m the ugliest TheEmperor\'s guard ◟(๑･ิټ･ิ๑)◞}',
'Securinets{Siiiir, please return to where you get from. This is a respectable place guarded by TheEmperor\'s guards ( ಠ ͜ʖರೃ)}',
'Securinets{Are you a hacker that wants to get TheEmperor\'s flag? We, his guards, will not be allowing such thing ( ͡ಠ ͜ʖ ͡ಠ)}',
'Securinets{Horraaaaay, a hacker that wants to be arrested seems to be caught \ (•◡•) /}',
'Securinets{Do you want to pick a fight with me? One of TheEmperor\'s guards? (ง ͠° ͟ل͜ ͡°)ง}',
'Securinets{I\'m very strong as TheEmperor\'s guard (•̀ᴗ•́)و ̑̑}',
'Securinets{Lunch time ( ━☞´◔‿ゝ◔`)━☞}',
'Securinets{What the hell are you? ( ͝סּ ͜ʖ͡סּ)}',
'Securinets{Was the first word that came into your mind was "cute" when you just saw me? (◕‿◕✿)}',
'Securinets{Do you want to give me your number... Hacker? ◕‿↼}',
'Securinets{What do you think about my new hair cut? ξξ(∵◕◡◕∵)ξξ}',
'Securinets{You are not supposed to be here... ◔̯◔}',
'Securinets{What the hell is happening here ಠ_ಠ}',
'Securinets{I don\'t want to be TheEmperor\'s guard (ᗒᗣᗕ)՞}',
'Securinets{I\'m gonna kill you (つ◉益◉)つ}',
'Securinets{You don\'t know that I\'m TheEmperor\'s guard right? ლಠ益ಠ)ლ}',
'Securinets{Finally... a hacker that\'s going to be caputred ͡ಥ ͜ʖ ͡ಥ}',
'Securinets{Don\'t move! Hacker! ̿̿’̿’\̵͇̿̿\=(•̪●)=/̵͇̿̿/’̿̿ ̿ ̿ ̿}',
'Securinets{Hey Hacker join us in TheEmperor\'s party ( ^​_^）o自自o（^_​^ )}',
'Securinets{Any last wish before you die? ╾━╤デ╦︻(▀̿Ĺ̯▀̿ ̿)}',
'Securinets{Who served me this stinky food? (╯°o°）╯︵ ┻━┻}',
'Securinets{I don\'t want to stay around this table (ノಠ益ಠ)ノ彡┻━┻}',
'Securinets{Do you believe if I told you that I\'m the strongest TheEmperor\'s guard? ᕙᓄ(☉ਊ☉)ᓄᕗ}',
'Securinets{Honey, I hope you enjoy the Spaghetti code that I\'ve prepared ┣┓웃┏♨❤♨┑유┏┥}',
'Securinets{Flagus disappearus as if it became invisibilus (∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ. *}',
'Securinets{I can hear someone is near me. It\'s true that I\'m a blind guard serving TheEmperor but I can hear you ┌(▼▼)}',
'Securinets{Ultra instinct mode enabled ⊹╰(⌣ʟ⌣)╯⊹}',
'Securinets{What do you think about these muscles? Am I the strongest among TheEmperor\'s guards? ᕦ(⩾﹏⩽)ᕥ}',
'Securinets{I brought some food. The night is too long for me as TheEmperor\'s guard ♨(⋆‿⋆)♨}',
'Securinets{If someone see a hacker please wake me up. I need some rest as TheEmperor\'s guard (¦ꄰ[▓▓]}',
'Securinets{This sword battle will end only if someone die and I, TheEmperor\'s guard, will be the winner Ｏ( ｀_´)乂(｀_´ )Ｏ}',
'Securinets{Put your hands up in the air you hacker. I\'m TheEmperor\'s guard and you\'re under arrest ━╤デ╦︻(▀̿̿Ĺ̯̿̿▀̿ ̿)}',
'Securinets{Don\'t move hacker or I\'ll shoot you ( う-´)づ︻╦̵̵̿╤── \(˚☐˚”)/}'
];

var ol = window['console']['log'];
var fl = function(argument) {
    ol(guards[getRndInteger(0,guards.length-1)]);
}
var oa = window['alert'];
var fa = function(argument) {
  if(argument!="Welcome to the Empire. TheEmperor granted you an exceptional access with this flag" && argument!="Wrong password! You don't have TheEmperor's approval in his Empire without the correct password"){
    oa(guards[getRndInteger(0,guards.length-1)]);
  }else{
    oa(argument);
  }
}
window['console']['log'] = fl;
window['alert'] = fa;
function validateform(){  
var password=document.myform.password.value;  

flag=[
"Securinets{Congratulations}",
"Securinets{This_might_be_the_flag}",
"Securinets{flag}",
"Securinets{gg_ez}",
"Securinets{good_work)",
"Securinets{This_is_not_the_flag}",
"Securinets{After_trying_this_flag_you_will_know_that_its_incorrect}",
"Securinets{There_is_a_small_chance_this_might_be_the_flag_that_youre_looking_for}",
"Securinets{Kill_TheEmperor_and_you_will_control_the_empire}",
"Securinets{Dont_try_all_these_flags_or_you_will_get_banned}",
"Securinets{This_is_the_flag_._Is_this_what_you_want_to_read?_then_nope}",
"Securinets{Tell_me_where_is_the_real_flag_and_I_will_spare_your_life}",
"Securinets{What_are_you_doing_here?}",
"Securinets{Heehee_you_will_never_be_able_to_validate_this_task_if_you_keep_brute_forcing_all_these_flags}",
"Securinets{NotEasy_enough_to_be_caught}",
"Securinets{Ten_mega_what_the_hell_is_this}",
"Securinets{Tellme_where_is_the_real_flag_please}",
"Securinets{Flag_brothers_code_will_never_be_understandable}",
"Securinets{Enjoy_your_luck_moments}",
"Securinets{I_hate_breaking_anything_especially_if_its_not_mine}",
"Securinets{Do_you_<3_me_as_much_as_i_<3_you?}",
"Securinets{All_these_games_are_amazing_and_I_like_simple_they_are}",
"Securinets{Probably_borrowing_a_pen_from_my_classmate_will_not_hear_him}",
"Securinets{Do_you_see_baby_sharks_never_dududuru_...}",
"Securinets{This_is_real_newspaper}",
"Securinets{Flag_are_you_italien}",
"Securinets{Hello_world_see_you_later_in_another_isekai}",
"Securinets{Am_bored_probably_because_am_bored}",
"Securinets{Yo_this_is_not_flower_nor_vegetable}",
"Securinets{Flag_or_flag_is_zeus_belongs}",
"Securinets{My_flag_s_not_yours_do_you_believe_this?_i_dont_think}",
"Securinets{When_I_pee_i_need_16seconds_as_a_maximum_time_range_to_finish_what_about_you?}",
"Securinets{Waiting_for_the_flag_4ever_and_ever}",
"Securinets{Bye_crual_world_more_ifones_and_less_android}",
"Securinets{This_is_getting_ridicul3us_because_i_dont_want_to_share_the_flag_easily}",
"Securinets{Toootooooot_just_as_twenty_trains_passing_by}",
"Securinets{I_believe_there_is_noo_flying_cars_here}",
"Securinets{Im_tired_from_hiding_it_in_this_array_but_you_cant_find_it_easily}",
"Securinets{Never_gonna_give_you_up_hihihihi_are_you_rock_and_rolled_?_im_joking}",
"Securinets{Dont_waste_your_time_withthin_this_array_for_hints_its_a_waste_of_time}",
"Securinets{Hunting_for_the_real_flag_not_hunting_for_hints}",
"Securinets{Once_upon_a_time_a_greedy_bee_that_wants_to_be_the_queen_but_nodoby_knows_whether_she_became_the_queen_or_not",
"Securinets{Are_you_readyyyyyy_to_get_the_ghost_flag_?}",
"Securinets{Its_me_TheEmeror_well_what_does_3_APT_groups_do_in_a_compromised_server?}",
"Securinets{You_will_never_find_any_clue_here_by_reading_these_flags}",
"Securinets{Do_you_know_that_TheEmperor_liked_Empowering_his_voice_and_singing_?}",
"Securinets{Now_we_know_my_ABC_tell_me_how_my_empowered_flag_flee_of_me}",
"Securinets{Do_you_want_to_build_a_snowmaaaan_?_probably_you_need_more_the_flaaaaag_?",
"Securinets{If_youre_still_looking_the_flag_here_i_can_guarantee_that_you_can_start_loosing_your_faith_on_your_instinct_here}",
"Securinets{Im_a_barby_girl_in_a_barby_woooooorld_round_and_robin_ah_ah_yeah}",
"Securinets{You_lost_I_told_you_the_flag_is_not_here_at_all}",
"Securinets{Well_you_dont_know_which_one_is_the_flag}"
];
var correct=true;
for(var i=0;i<flag.length;i++){
  if (password[i]==flag[i][i]){
  }else{
    correct=false;
    alert("Wrong password! You don't have TheEmperor's approval in his Empire without the correct password");  
	break;
  }
}
if(correct)alert("Welcome to the Empire. TheEmperor granted you an exceptional access with this flag");
return false;
}