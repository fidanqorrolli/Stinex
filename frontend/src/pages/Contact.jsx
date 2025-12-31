import React, { useState } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Textarea } from "../components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { useToast } from "../hooks/use-toast";
import { contactAPI } from "../services/api";
import { 
  Phone, 
  Mail, 
  MapPin, 
  Clock,
  Send,
  CheckCircle
} from "lucide-react";

const Contact = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    service: "",
    message: ""
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSelectChange = (value) => {
    setFormData(prev => ({
      ...prev,
      service: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      // Submit to real backend API
      const response = await contactAPI.submitContact(formData);
      
      console.log("Contact form submitted successfully:", response);
      
      toast({
        title: "Nachricht gesendet!",
        description: response.message || "Vielen Dank für Ihre Anfrage. Wir melden uns binnen 24 Stunden bei Ihnen.",
      });
      
      // Reset form after successful submission  
      setFormData({
        name: "",
        email: "",
        phone: "",
        service: "",
        message: ""
      });
      
    } catch (error) {
      console.error("Error submitting contact form:", error);
      
      toast({
        title: "Fehler beim Senden",
        description: error.message || "Es gab ein Problem beim Senden Ihrer Nachricht. Bitte versuchen Sie es erneut.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const contactInfo = [
    {
      icon: Phone,
      title: "Telefon",
      content: "+49 123 456 789",
      description: "Mo-Fr: 8:00 - 18:00 Uhr"
    },
    {
      icon: Mail,
      title: "E-Mail",
      content: "info@stinex.de",
      description: "Wir antworten binnen 24h"
    },
    {
      icon: MapPin,
      title: "Adresse",
      content: "Musterstraße 123, 20095 Hamburg",
      description: "Unser Hauptsitz"
    },
    {
      icon: Clock,
      title: "Öffnungszeiten",
      content: "Mo-Fr: 8:00 - 18:00",
      description: "Sa: 9:00 - 16:00"
    }
  ];

  const services = [
    "Büroreinigung",
    "Wohnungsreinigung", 
    "Gewerbereinigung",
    "Grundreinigung",
    "Einmalige Reinigung",
    "Fensterreinigung",
    "Sonstiges"
  ];

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Kontakt
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Haben Sie Fragen oder möchten Sie ein unverbindliches Angebot? 
            Wir freuen uns auf Ihre Nachricht und melden uns schnellstmöglich bei Ihnen.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-12">
          {/* Contact Form */}
          <div className="lg:col-span-2">
            <Card className="shadow-lg">
              <CardHeader>
                <CardTitle className="text-2xl">Nachricht senden</CardTitle>
                <CardDescription>
                  Füllen Sie das Formular aus und wir melden uns innerhalb von 24 Stunden bei Ihnen.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="name">Name *</Label>
                      <Input
                        id="name"
                        name="name"
                        type="text"
                        required
                        value={formData.name}
                        onChange={handleInputChange}
                        placeholder="Ihr vollständiger Name"
                        className="mt-1"
                        disabled={isSubmitting}
                      />
                    </div>
                    <div>
                      <Label htmlFor="email">E-Mail *</Label>
                      <Input
                        id="email"
                        name="email"
                        type="email"
                        required
                        value={formData.email}
                        onChange={handleInputChange}
                        placeholder="ihre.email@beispiel.de"
                        className="mt-1"
                        disabled={isSubmitting}
                      />
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="phone">Telefon</Label>
                      <Input
                        id="phone"
                        name="phone"
                        type="tel"
                        value={formData.phone}
                        onChange={handleInputChange}
                        placeholder="+49 123 456 789"
                        className="mt-1"
                        disabled={isSubmitting}
                      />
                    </div>
                    <div>
                      <Label htmlFor="service">Gewünschte Leistung</Label>
                      <Select 
                        onValueChange={handleSelectChange} 
                        value={formData.service}
                        disabled={isSubmitting}
                      >
                        <SelectTrigger className="mt-1">
                          <SelectValue placeholder="Leistung auswählen" />
                        </SelectTrigger>
                        <SelectContent>
                          {services.map((service, index) => (
                            <SelectItem key={index} value={service}>
                              {service}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="message">Nachricht *</Label>
                    <Textarea
                      id="message"
                      name="message"
                      required
                      value={formData.message}
                      onChange={handleInputChange}
                      placeholder="Beschreiben Sie Ihre Anfrage oder teilen Sie uns Details zu Ihrem Reinigungsbedarf mit..."
                      rows={6}
                      className="mt-1"
                      disabled={isSubmitting}
                    />
                  </div>

                  <Button 
                    type="submit" 
                    className="w-full bg-emerald-600 hover:bg-emerald-700 text-lg py-3 h-auto"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Wird gesendet...
                      </>
                    ) : (
                      <>
                        <Send className="mr-2 h-4 w-4" />
                        Nachricht senden
                      </>
                    )}
                  </Button>

                  <p className="text-sm text-gray-500 text-center">
                    * Pflichtfelder. Ihre Daten werden vertraulich behandelt und nicht an Dritte weitergegeben.
                  </p>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Contact Information */}
          <div className="space-y-6">
            <Card className="shadow-lg">
              <CardHeader>
                <CardTitle>Kontaktinformationen</CardTitle>
                <CardDescription>
                  So erreichen Sie uns direkt
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {contactInfo.map((info, index) => {
                  const Icon = info.icon;
                  return (
                    <div key={index} className="flex items-start space-x-3">
                      <div className="w-10 h-10 bg-emerald-600 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Icon className="h-5 w-5 text-white" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{info.title}</h3>
                        <p className="text-blue-600 font-medium">{info.content}</p>
                        <p className="text-sm text-gray-500">{info.description}</p>
                      </div>
                    </div>
                  );
                })}
              </CardContent>
            </Card>

            {/* Service Areas */}
            <Card className="shadow-lg">
              <CardHeader>
                <CardTitle>Servicegebiete</CardTitle>
                <CardDescription>
                  In diesen Bereichen sind wir für Sie da
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {[
                    "Hamburg und Umgebung",
                    "Norderstedt, Ahrensburg",
                    "Pinneberg, Elmshorn", 
                    "Lüneburg, Stade",
                    "Auf Anfrage: weitere Gebiete"
                  ].map((area, index) => (
                    <div key={index} className="flex items-center">
                      <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                      <span className="text-gray-600">{area}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Emergency Contact */}
            <Card className="shadow-lg border-orange-200 bg-orange-50">
              <CardHeader>
                <CardTitle className="text-orange-900">Notfall-Service</CardTitle>
                <CardDescription className="text-orange-700">
                  24/7 erreichbar für dringende Fälle
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <Phone className="h-8 w-8 text-orange-600 mx-auto mb-2" />
                  <p className="font-bold text-xl text-orange-900">+49 123 456 000</p>
                  <p className="text-sm text-orange-700 mt-2">
                    Für Wasserschäden, Reinigungsnotfälle und dringende Termine
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Map Placeholder */}
        <div className="mt-16">
          <Card className="shadow-lg">
            <CardContent className="p-0">
              <div className="bg-gray-200 h-96 rounded-lg flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <MapPin className="h-12 w-12 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Standort Hamburg</h3>
                  <p>Musterstraße 123, 20095 Hamburg</p>
                  <p className="text-sm mt-2">Interaktive Karte wird hier angezeigt</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Contact;