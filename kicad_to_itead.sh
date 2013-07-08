## KiCAD gerber format to ITEAD renamer
## http://jaanus.tech-thing.org

#loop through all files
for f in *
do
   if [ "${f: -9}" == "-Back.gbl" ]
   then
      mv -v "$f" "${f:0: -9}.GBL"
   fi

   if [ "${f: -10}" == "-Front.gtl" ]
   then
      mv -v "$f" "${f:0: -10}.GTL"
   fi
   
   if [ "${f: -15}" == "-Mask_Front.gts" ]
   then
      mv -v "$f" "${f:0: -15}.GTS"
   fi

   if [ "${f: -14}" == "-Mask_Back.gbs" ]
   then
      mv -v "$f" "${f:0: -14}.GBS"
   fi
   
   if [ "${f: -16}" == "-SilkS_Front.gto" ]
   then
      mv -v "$f" "${f:0: -16}.GTO"
   fi

   if [ "${f: -15}" == "-SilkS_Back.gbo" ]
   then
      mv -v "$f" "${f:0: -15}.GBO"
   fi

   if [ "${f: -4}" == ".drl" ]
   then
      mv -v "$f" "${f:0: -4}.TXT"
   fi

   if [ "${f: -14}" == "-PCB_Edges.gbr" ]
   then
      mv -v "$f" "${f:0: -14}.BOR"
   fi

   if [ "${f: -9}" == "-B_Cu.gbl" ]
   then
      mv -v "$f" "${f:0: -9}.GBL"
   fi

   if [ "${f: -9}" == "-F_Cu.gtl" ]
   then
      mv -v "$f" "${f:0: -9}.GTL"
   fi
   
   if [ "${f: -11}" == "-F_Mask.gts" ]
   then
      mv -v "$f" "${f:0: -11}.GTS"
   fi

   if [ "${f: -11}" == "-B_Mask.gbs" ]
   then
      mv -v "$f" "${f:0: -11}.GBS"
   fi
   
   if [ "${f: -12}" == "-F_SilkS.gto" ]
   then
      mv -v "$f" "${f:0: -12}.GTO"
   fi

   if [ "${f: -12}" == "-B_SilkS.gbo" ]
   then
      mv -v "$f" "${f:0: -12}.GBO"
   fi

   if [ "${f: -14}" == "-Edge_Cuts.gbr" ]
   then
      mv -v "$f" "${f:0: -14}.BOR"
   fi

done
