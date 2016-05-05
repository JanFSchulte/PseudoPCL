#include "TPaveText.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TText.h"
#include "TLegend.h"
#include "TStyle.h"

//int runno = 2549;

void PCLplot(int runno){

  gStyle->SetOptStat(1);

  TPaveText * tp1 = new TPaveText(0.45, 0.463014, 0.55, 0.536986,"NDCNB");
  tp1->SetBorderSize(0);
  tp1->SetFillStyle(0);
  tp1->SetFillColor(10);
  tp1->SetTextColor(1);
  tp1->SetTextFont(61);
  TText * text1 = tp1->AddText(Form("Run %i",runno));
  text1->SetTextSize(0.025);
  /*
  TPaveText * tp2 = new TPaveText(0.6, 0.463014, 0.7, 0.536986,"NDCNB");
  tp2->SetBorderSize(0);
  tp2->SetFillStyle(0);
  tp2->SetFillColor(10);
  tp2->SetTextColor(1);
  tp2->SetTextFont(61);
  TText * text2 = tp2->AddText(Form("Run %i",runno));
  text2->SetTextSize(0.025);
  */
  TFile * f = new TFile("PCL_SiPixAl_DQM.root");

  TCanvas * cPCL_SiPixAl = (TCanvas*) f->Get("PCL_SiPixAl");
  cPCL_SiPixAl->cd();
  cPCL_SiPixAl->Draw();
  cPCL_SiPixAl->SaveAs(Form("PCL_SiPixAl_%i.png",runno));
  cPCL_SiPixAl->Close();

  TCanvas * cPCL_SiPixAl_Expert = (TCanvas*) f->Get("PCL_SiPixAl_Expert");
  cPCL_SiPixAl_Expert->cd();
  cPCL_SiPixAl_Expert->Draw();
  tp1->Draw();
  //tp2->Draw();
  cPCL_SiPixAl_Expert->SaveAs(Form("PCL_SiPixAl_Expert_%i.png",runno));
  cPCL_SiPixAl_Expert->Close();   
}
